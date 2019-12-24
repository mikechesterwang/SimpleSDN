"""Topology Manager

track the network's topology from network events.

"""

from ryu.topology.switches import Port, Switch, Link
from Graph import Graph
from config import config_algorithm


class Device:
    """Base class to represent an device in the network.

    Any device (switch or host) has a name (used for debugging only)
    and a set of neighbors.
    """

    def __init__(self, name):
        self.name = name
        self.neighbors = {}

    def add_neighbor(self, mac, dev):
        self.neighbors[mac] = dev

    def __str__(self):
        return "{}({})".format(self.__class__.__name__,
                               self.name)


class TMSwitch(Device):
    """Representation of a switch, extends Device

    This class is a wrapper around the Ryu Switch object,
    which contains information about the switch's ports
    """

    def __init__(self, name, switch):
        super(TMSwitch, self).__init__(name)

        self.switch = switch
        self.mac_to_port = {}
        # Add more attributes as necessary

    def get_dpid(self):
        """Return switch DPID"""
        return self.switch.dp.id

    def get_ports(self):
        """Return list of Ryu port objects for this switch
        """
        return self.switch.ports

    def get_dp(self):
        """Return switch datapath object"""
        return self.switch.dp


class TMHost(Device):
    """Representation of a host, extends Device

    This class is a wrapper around the Ryu Host object,
    which contains information about the switch port to which
    the host is connected
    """

    def __init__(self, name, host):
        super(TMHost, self).__init__(name)

        self.host = host

    def get_mac(self):
        return self.host.mac

    def get_ips(self):
        return self.host.ipv4

    def get_port(self):
        """Return Ryu port object for this host"""
        return self.host.port


class TopoManager:
    """
    class for keeping track of the network topology

    """

    def __init__(self, sp_mode):
        # Initialize some data structures
        self.sp_mode = sp_mode
        self.abstract_graph = Graph()
        self.all_devices = {}
        self.all_switches = {}
        self.all_hosts = {}
        self.ip_to_mac = {}

    def add_switch(self, sw):

        name = "switch_{}".format(sw.dp.id)
        switch = TMSwitch(name, sw)

        self.all_devices[name] = switch
        self.all_switches[name] = switch

        # Add switch to some data structure(s)
        port_addresses = []
        for port in sw.ports:
            port_addresses.append(port.hw_addr)
            switch.mac_to_port[port.hw_addr] = port.port_no
        self.abstract_graph.addVertex(name, port_addresses)

    def delete_switch(self, sw):
        # 从所有设备中删除
        if "switch_{}".format(sw.dp.id) in self.all_devices.keys():
            self.all_devices.pop("switch_{}".format(sw.dp.id))

        # 从所有交换机中删除
        if "switch_{}".format(sw.dp.id) in self.all_switches.keys():
            self.all_switches.pop("switch_{}".format(sw.dp.id))

        # 从抽象图中删除
        self.abstract_graph.removeVertex("switch_{}".format(sw.dp.id))

    def add_host(self, h):

        name = "host_{}".format(h.mac)
        host = TMHost(name, h)

        self.all_devices[name] = host
        self.all_hosts[name] = host
        for ip in h.ipv4:
            self.ip_to_mac[ip] = h.mac

        # Add host to some data structure(s)
        self.abstract_graph.addVertex(name, [h.mac])

    def add_link(self, name1, mac1, name2, mac2):
        self.abstract_graph.addEdge(name1, name2, mac1, mac2)
        self.all_devices[name1].add_neighbor(mac1, self.all_devices[name2])
        self.all_devices[name2].add_neighbor(mac2, self.all_devices[name1])

    def delete_link(self, name1, mac1, name2, mac2):
        # 从抽象图中删除
        self.abstract_graph.removeEdge(name1, mac1)

        # 删除设备一中和设备二的连接
        if name1 in self.all_devices.keys():
            if mac1 in self.all_devices[name1].neighbors.keys():
                self.all_devices[name1].neighbors.pop(mac1)

        # 删除设备二中和设备一的连接
        if name2 in self.all_devices.keys():
            if mac2 in self.all_devices[name2].neighbors.keys():
                self.all_devices[name2].neighbors.pop(mac2)

    def change_interface_state(self, name, mac, state):
        self.abstract_graph.changeInterfaceState(name, mac, state)

    def get_mac_by_ip(self, ip):
        if ip in self.ip_to_mac.keys():
            return self.ip_to_mac[ip]
        else:
            return None

    def update_install(self):
        if self.sp_mode:
            self.abstract_graph.rs.use_spanning_tree = True
            this_dict = {}
            trans_dict = {}
            for sw in self.all_switches:
                this_dict = self.abstract_graph.rs.updateSpanningTree_BFS(sw)
                break
            for sw in self.all_switches:
                trans_dict[sw] = []
                for mac in this_dict[sw]:
                    if not this_dict[sw][mac]:
                        trans_dict[sw].append(self.all_switches[sw].mac_to_port[mac])
            this_list = []
            for h in self.all_hosts:
                self.abstract_graph.queryShortestPath(self.all_hosts[h].name)
            for sw in self.all_switches:
                this_map = self.abstract_graph.queryShortestPath(self.all_switches[sw].name)
                for key in this_map:
                    if 'host' in key:
                        data_path = self.all_switches[sw].get_dp()
                        if this_map[key] is None:
                            this_list.append((data_path, key[5:], None))
                        else:
                            this_list.append((data_path, key[5:], self.all_switches[sw].mac_to_port[this_map[key]]))
            return this_list, trans_dict
        else:
            self.abstract_graph.rs.use_spanning_tree = False
            this_list = []
            for h in self.all_hosts:
                self.abstract_graph.queryShortestPath(self.all_hosts[h].name, model=config_algorithm)
            for sw in self.all_switches:
                this_map = self.abstract_graph.queryShortestPath(self.all_switches[sw].name, model=config_algorithm)
                for key in this_map:
                    if 'host' in key:
                        data_path = self.all_switches[sw].get_dp()
                        if this_map[key] is None:
                            this_list.append((data_path, key[5:], None))
                        else:
                            this_list.append((data_path, key[5:], self.all_switches[sw].mac_to_port[this_map[key]]))
            return this_list

    def print_shortest_path(self, src, dst):
        try:
            result = self.abstract_graph.print_path("host_{}".format(src), "host_{}".format(dst))
            print(result)
        except KeyError:
            print('no path.')

    def print_topology(self):
        if self.sp_mode:
            result = 'Topology:\r\n'
            result = result + self.abstract_graph.print_topology()
            result = result + '\r\nSpanning Tree\r\n'
            result = result + self.abstract_graph.print_spanning_tree()
        else:
            result = self.abstract_graph.print_topology()

        print(result)
