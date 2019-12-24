#!/usr/bin/env python3

"""Shortest Path Switching

creates a simple controller application that watches for
topology events.

"""

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

from ryu.topology import event, switches
import ryu.topology.api as topo

from ryu.lib.packet import packet, ether_types
from ryu.lib.packet import ethernet, arp, icmp

from ofctl_utils import OfCtl, VLANID_NONE

from topo_manager import TopoManager


class ShortestPathSwitching(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ShortestPathSwitching, self).__init__(*args, **kwargs)

        self.loop_mode = True
        self.sp_mode = self.loop_mode and True
        self.tm = TopoManager(self.sp_mode)
        self.port_map = {'switch_1': [1, 2], 'switch_2': [1, 2, 3], 'switch_3': [1, 2]}

    @set_ev_cls(event.EventSwitchEnter)
    def handle_switch_add(self, ev):
        """
        Event handler indicating a switch has come online.
        """
        switch = ev.switch

        self.logger.warn("Added Switch switch%d with ports:", switch.dp.id)
        for port in switch.ports:
            self.logger.warn("\t%d:  %s", port.port_no, port.hw_addr)

        # Update network topology and flow rules
        self.tm.add_switch(switch)
        self.install_all()

    @set_ev_cls(event.EventSwitchLeave)
    def handle_switch_delete(self, ev):
        """
        Event handler indicating a switch has been removed
        """
        switch = ev.switch

        self.logger.warn("Removed Switch switch%d with ports:", switch.dp.id)
        for port in switch.ports:
            self.logger.warn("\t%d:  %s", port.port_no, port.hw_addr)

        # Update network topology and flow rules
        self.tm.delete_switch(switch)
        self.install_all()

    @set_ev_cls(event.EventHostAdd)
    def handle_host_add(self, ev):
        """
        Event handler indiciating a host has joined the network
        This handler is automatically triggered when a host sends an ARP response.
        """
        host = ev.host
        self.logger.warn("Host Added:  %s (IPs:  %s) on switch%s/%s (%s)",
                         host.mac, host.ipv4,
                         host.port.dpid, host.port.port_no, host.port.hw_addr)

        # Update network topology and flow rules
        self.tm.add_host(host)
        self.tm.add_link("host_{}".format(host.mac), host.mac,
                         "switch_{}".format(host.port.dpid), host.port.hw_addr)
        self.install_all()

    @set_ev_cls(event.EventLinkAdd)
    def handle_link_add(self, ev):
        """
        Event handler indicating a link between two switches has been added
        """
        link = ev.link
        src_port = ev.link.src
        dst_port = ev.link.dst
        self.logger.warn("Added Link:  switch%s/%s (%s) -> switch%s/%s (%s)",
                         src_port.dpid, src_port.port_no, src_port.hw_addr,
                         dst_port.dpid, dst_port.port_no, dst_port.hw_addr)

        # Update network topology and flow rules
        self.tm.add_link("switch_{}".format(src_port.dpid), src_port.hw_addr,
                         "switch_{}".format(dst_port.dpid), dst_port.hw_addr)
        self.install_all()

    @set_ev_cls(event.EventLinkDelete)
    def handle_link_delete(self, ev):
        """
        Event handler indicating when a link between two switches has been deleted
        """
        link = ev.link
        src_port = link.src
        dst_port = link.dst

        self.logger.warn("Deleted Link:  switch%s/%s (%s) -> switch%s/%s (%s)",
                         src_port.dpid, src_port.port_no, src_port.hw_addr,
                         dst_port.dpid, dst_port.port_no, dst_port.hw_addr)

        # Update network topology and flow rules
        self.tm.delete_link("switch_{}".format(src_port.dpid), src_port.hw_addr,
                            "switch_{}".format(dst_port.dpid), dst_port.hw_addr)
        self.install_all()

    @set_ev_cls(event.EventPortModify)
    def handle_port_modify(self, ev):
        """
        Event handler for when any switch port changes state.
        This includes links for hosts as well as links between switches.
        """
        port = ev.port
        self.logger.warn("Port Changed:  switch%s/%s (%s):  %s",
                         port.dpid, port.port_no, port.hw_addr,
                         "UP" if port.is_live() else "DOWN")

        # Update network topology and flow rules
        self.tm.change_interface_state("switch_{}".format(port.dpid), port.hw_addr, port.is_live())
        self.install_all()

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        """
        EventHandler for PacketIn messages
        """
        msg = ev.msg
        pkt = packet.Packet(data=msg.data)
        pkt_ethernet = pkt.get_protocol(ethernet.ethernet)
        if not pkt_ethernet:
            return

        if pkt_ethernet.ethertype == 35020:
            return

        # In OpenFlow, switches are called "datapaths".  Each switch gets its own datapath ID.
        # In the controller, we pass around datapath objects with metadata about each switch.
        dp = msg.datapath

        # Use this object to create packets for the given datapath
        ofctl = OfCtl.factory(dp, self.logger)

        in_port = msg.in_port
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_ARP:
            # print('arp packet in!!')
            arp_msg = pkt.get_protocols(arp.arp)[0]

            if arp_msg.opcode == arp.ARP_REQUEST:
                self.logger.warning("Received ARP REQUEST on switch%d/%d:  Who has %s?  Tell %s",
                                    dp.id, in_port, arp_msg.dst_ip, arp_msg.src_mac)

                # Generate a *REPLY* for this request based on your switch state
                result_mac = self.tm.get_mac_by_ip(arp_msg.dst_ip)
                if result_mac is not None:
                    # 如果mac地址存在，则返回包
                    print('%s to %s' % (arp_msg.dst_ip, result_mac))
                    ofctl.send_arp(arp_opcode=arp.ARP_REPLY,
                                   vlan_id=VLANID_NONE,
                                   dst_mac=arp_msg.src_mac,
                                   sender_mac=result_mac,
                                   sender_ip=arp_msg.dst_ip,
                                   target_mac=arp_msg.src_mac,
                                   target_ip=arp_msg.src_ip,
                                   src_port=ofctl.dp.ofproto.OFPP_CONTROLLER,
                                   output_port=msg.in_port)
                    self.tm.print_shortest_path(arp_msg.src_mac, result_mac)
                else:
                    if not self.loop_mode:
                        print('this mac not exits.')
                        return
                    # 如果mac地址不存在，则泛洪
                    msg = ev.msg
                    data = msg.data
                    datapath = msg.datapath
                    # print(dp.id)
                    ofproto = datapath.ofproto
                    ofp_parser = datapath.ofproto_parser

                    if self.sp_mode:
                        if "switch_{}".format(dp.id) in self.port_map.keys():
                            actions = []
                            for p in self.port_map["switch_{}".format(dp.id)]:
                                if p != msg.in_port:
                                    # print(msg.in_port, p)
                                    actions.append(ofp_parser.OFPActionOutput(p))
                        else:
                            actions = [ofp_parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                    else:
                        actions = [ofp_parser.OFPActionOutput(ofproto.OFPP_FLOOD)]

                    out = ofp_parser.OFPPacketOut(
                        datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
                        actions=actions, data=data)
                    datapath.send_msg(out)

    def install_all(self):
        if self.sp_mode:
            this_list, trans_dict = self.tm.update_install()
            self.port_map = trans_dict
            for item in this_list:
                if item[2] is None:
                    self.delete_forwarding_rule(item[0], item[1])
                else:
                    self.add_forwarding_rule(item[0], item[1], item[2])
        else:
            this_list = self.tm.update_install()
            for item in this_list:
                if item[2] is None:
                    self.delete_forwarding_rule(item[0], item[1])
                else:
                    self.add_forwarding_rule(item[0], item[1], item[2])
        self.tm.print_topology()

    def add_forwarding_rule(self, datapath, dl_dst, port):
        ofctl = OfCtl.factory(datapath, self.logger)

        actions = [datapath.ofproto_parser.OFPActionOutput(port)]
        ofctl.set_flow(cookie=0,
                       priority=0,
                       dl_type=ether_types.ETH_TYPE_IP,
                       dl_vlan=VLANID_NONE,
                       dl_dst=dl_dst,
                       actions=actions)

    def delete_forwarding_rule(self, datapath, dl_dst):
        ofctl = OfCtl.factory(datapath, self.logger)

        match = datapath.ofproto_parser.OFPMatch(dl_dst=dl_dst)
        ofctl.delete_flow(cookie=0, priority=0, match=match)