from RouteScheduler import *
# 
# Copyright (c) 2019 Mike Chester Wang, Hui OUYANG, Yongning CAI
# This code is distributed under SB license
# 
# SB LICENSE
# Dec. 21st 2019
# Anyone who copy our code to submit his/her homework is SB.
#
# TERMS
# 0. Do you own job.
#
class Vertex(object):
    def __init__(self, vid, interface_ids):
        """
        vid, interface_ids\r\n
        初始化参数: 结点的id, 以及结点的接口的id数组; \r\n
        这些id以键值形式存放在dict中，可以不用为从0开始的连续id
        """
        self.id = vid
        self.interfaces = {}
        self.edges = {}
        for iid in interface_ids:
            self.interfaces[iid] = True

    def addEdge(self, mac, e):
        self._edges[mac] = e
    
    def __str__(self):
        return str(self.id)

class Edge(object):
    def __init__(self, v1_id, v2_id, v1_interface, v2_interface):
        """
        v1_id, v2_id, v1_interface, v2_interface\r\n
        初始化参数: 两个结点的id，以及两个结点的接口id\r\n
        这些id以键值形式存放在dict中，可以不用为从0开始的连续id
        """
        self.v1_id = v1_id
        self.v2_id = v2_id
        self.v1_inerface = v1_interface
        self.v2_inerface = v2_interface

    def __str__(self):
        return "(" + self.v1_id +"," + self.v2_id + ")"
    

class Graph(object):

    def __init__(self):
        self._vertices = {}
        self._edges = {}
        self.edge_hash = 0
        self.rs = RouteSchduler(self)

    def changeInterfaceState(self, v1_id, v1_interface_id, state):
        """
        改变指定结点的接口的状态, True为打开(link up)，False为关闭(link down)
        """
        self._vertices[v1_id].interfaces[v1_interface_id] = state

    def addEdge(self, v1_id, v2_id, v1_interface, v2_interface):
        """
        初始化参数: 两个结点的id，以及两个结点的接口id\r\n
        这些id以键值形式存放在dict中，可以不用为从0开始的连续id
        """
        v1 = self._vertices[v1_id]
        v2 = self._vertices[v2_id]

        # Instantiate new edge
        e = Edge(v1_id, v2_id, v1_interface, v2_interface)

        # Update global table
        self._edges[self.edge_hash] = e
        
        # Add edges to vertices
        v1.edges[v1_interface] = self.edge_hash
        v2.edges[v2_interface] = self.edge_hash

        self.edge_hash += 1

    def removeEdge(self, vid, interface_id):
        """
        根据提供的vid和interface_id删除一个Edge 
        """
        if not (vid in self._vertices and interface_id in self._vertices[vid].edges):
            return None
        edge_hash_id = self._vertices[vid].edges[interface_id]
        e:Edge = self._edges[edge_hash_id]
        if e.v1_id in self._vertices and e.v1_inerface in self._vertices[e.v1_id].edges:
            del self._vertices[e.v1_id].edges[e.v1_inerface]

        if e.v2_id in self._vertices and e.v2_inerface in self._vertices[e.v2_id].edges:
            del self._vertices[e.v2_id].edges[e.v2_inerface]

        if edge_hash_id in self._edges:
            del self._edges[edge_hash_id]
        
        
    def addVertex(self, vid, interface_ids):
        """
        添加一个结点，结点的id为指定的id\r\n
        结点的接口的id为interface_ids数组指定的id; 接口默认为True(打开)\r\n
        """
        v = Vertex(vid, interface_ids)
        self._vertices[vid] = v
    
    def removeVertex(self, vid):
        """
        根据结点id删除一个switch或host\r\n
        同时删除与它相连的所有边
        """
        # Delete edges conneting to this vertex
        for edge_hash_id in self._vertices[vid].edges.keys():
            if edge_hash_id in self._edges:
                e = self._edges[edge_hash_id]
                if e.v1_id in self._vertices:
                    v1:Vertex = self._vertices[e.v1_id]
                    del v1.edges[e.v1_inerface]
                if e.v2_id in self._vertices:
                    v2:Vertex = self._vertices[e.v2_id]
                    del v2.edges[e.v2_interface]

                del self._edges[edge_hash_id]
        
        # Delete this vertex
        if vid in self._vertices:
            del self._vertices[vid]    

    def _has_edge(self, hash_id):
        return hash_id in self._edges

    def _interface_clear(self, vid, interface_id):
        """
        Estimate whether this interface is connecting to another vertex and both interfaces are on
        """
        v:Vertex = self._vertices[vid]
        if not interface_id in v.edges:
             return False # No link connecting to this interface

        e:Edge = self._edges[v.edges[interface_id]]
        if not (e.v1_id in self._vertices and e.v2_id in self._vertices):
            return False # Vertices of the given edge is already removed

        v1:Vertex = self._vertices[e.v1_id]
        v2:Vertex = self._vertices[e.v2_id]
        return v1.interfaces[e.v1_inerface] and v2.interfaces[e.v2_inerface] # Whether both of the interfaces are on

    def _get_next_interfaceid(self, vid, interface_id):
        """
        Get the interface id of the opposite side of the given interface\r\n
        Return None if packet cannot forward through this given interface
        """
        if not self._interface_clear(vid, interface_id):
            return None # Packet cannot forward through this interface
        e:Edge = self._edges[self._vertices[vid].edges[interface_id]]
        return e.v1_inerface if e.v2_inerface == interface_id else e.v1_inerface

    def _get_next_vertexid(self, vid, interface_id):
        """
        Get the vid of the vertex in the opposite side of the given interface\r\n
        Return None if packet cannot forward through this given interface
        """
        if not self._interface_clear(vid, interface_id):
            return None # Packet cannot forward through this interface

        e:Edge = self._edges[self._vertices[vid].edges[interface_id]]
        v2_id = e.v1_id if e.v2_id == vid else e.v2_id
        return v2_id
        
    def queryShortestPath(self, vid, model='BFS', weight_dict=None):
        """
        `参数`:\r\n
        vid: src结点id\r\n
        model: 使用的模型, 默认为BFS; 可选BFS或Dijkstra\r\n
        weight_dict: 加权最短路图(用于加权最短路算法), 默认为None\r\n
        =======================================\r\n
        `返回`:\r\n
        BFS:\r\n
        flow table字典\r\n
        Dijkstra:\r\n
        距离字典, flow table字典\r\n
        =======================================\r\n
        `flow table`字典\r\n
        {int:int}\r\n
        内容为vid : interface_id\r\n
        =======================================\r\n
        `Dijkstra模型的weight_dict格式`\r\n
        weight_dict[vid][interface_id] = weight (单向边权)\r\n
        例如:\r\n
        10.0.0.1与10.0.0.2通过端口11:11:11:11:11:11和22:22:22:22:22:22相连\r\n
        那么，我们认为，packet从10.0.0.1出发到10.0.0.2的权值，与从10.0.0.2到10.0.0.1的权值可以不同\r\n
        图例:\r\n
        |10.0.0.1|->11:11:11:11:11:11->------->|10.0.0.2|\r\n
        |10.0.0.1|<-------<-22:22:22:22:22:22<-|10.0.0.2|\r\n
        格式:\r\n
        weight_dict['10.0.0.1']['11:11:11:11:11:11'] = 10\r\n
        weight_dict['10.0.0.2']['22:22:22:22:22:22'] = 20\r\n
        """
        
        if model == 'BFS':
            return self.rs.queryShortestPath_BFS(vid)
        elif model == 'Dijkstra':
            return self.rs.queryShortestPath_Dijkstra(vid, weight_dict)
        else:
            raise Exception("{model}model not exists.")
        
    def print_path(self, src_id, dst_id):
        v:Vertex = self._vertices[src_id]
        path = str(v.id)
        while v.id != dst_id:
            path += " => "
            next_interface_id = self.rs.rtn_cache[v.id][dst_id]
            v = self._vertices[self._get_next_vertexid(v.id, next_interface_id)]
            path += v.id
        return path

    def print_spanning_tree(self):
        rtn = ""
        v:Vertex = None
        e:Edge = None
        for v in self._vertices.values():
            rtn += v.id + "\n"
            for eid in v.edges.values():
                e = self._edges[eid]
                if(self.rs.blocked[e.v1_id][e.v1_inerface]):
                    continue
                rtn += "Edge: {}({}) <-> {}({})\n".format(e.v1_id, e.v1_inerface, e.v2_id, e.v2_inerface)
        return rtn

    def print_topology(self):
        rtn = ""
        v:Vertex = None
        e:Edge = None
        for v in self._vertices.values():
            rtn += v.id + "\n"
            for eid in v.edges.values():
                e = self._edges[eid]
                rtn += "Edge: {}({}) <-> {}({})\n".format(e.v1_id, e.v1_inerface, e.v2_id, e.v2_inerface)
        return rtn
    

    