from Graph import *
from DataStructure import *

INFINITY = 1_000_000_000
weight_delta = 0

class RouteSchduler(object):
    def __init__(self, graph):
        self.graph:Graph = graph
        self.blocked = {}
        self.rtn_cache = {}
        self.use_spanning_tree = False

    def updateSpanningTree_BFS(self, root_vid):

        def getNeighbor(e, vid):
            return self.graph._vertices[e.v1_id] if e.v2_id == vid else self.graph._vertices[e.v2_id]

        # update blocked interface table
        for vid in self.graph._vertices.keys():
            self.blocked[vid] = {}
            for iid in self.graph._vertices[vid].interfaces.keys():
                self.blocked[vid][iid] = True

        # varaibles
        visited = {}
        last_out_interface = {}
        MST_E = set()

        # init
        q = Queue()
        for v in self.graph._vertices.values():
            visited[v] = False
            last_out_interface[v] = None

        # BFS
        q.enQueue(self.graph._vertices[root_vid])
        while not q.isEmpty():
            u:Vertex = q.deQueue()
            for interface_id in u.edges.keys():
                e_hash_id = u.edges[interface_id]
                e = self.graph._edges[e_hash_id]
                getNeighbor(e, u.id)
                next_v = getNeighbor(e, u.id)
                
                if visited[next_v]:
                    continue

                MST_E.add(e)
                
                if last_out_interface[u] == None:
                    last_out_interface[next_v] = interface_id
                else:
                    last_out_interface[next_v] = last_out_interface[u]

                q.enQueue(next_v)
                visited[next_v] = True
        
        rtn = {}
        for v in last_out_interface.keys():
            rtn[v.id] = last_out_interface[v]
        self.rtn_cache[vid] = rtn

        for e in MST_E:
            self.blocked[e.v1_id][e.v1_inerface] = False
            self.blocked[e.v2_id][e.v2_inerface] = False

        return self.blocked

    def queryShortestPath_Dijkstra(self, vid, weight_dict=None):
        """
        Format of weight_dict:\r\n
        weight_dict[vid][interface_id] = weight (directed weight)\r\n
        e.g.:\r\n
        10.0
        10.0.0.1 is connected with 10.0.0.2 through 11:11:11:11:11:11 and 22:22:22:22:22:22\r\n
        We consider the weight from 10.0.0.1 to 10.0.0.2 is different from the weight from 10.0.0.2 to 10.0.0.1
        Example:\r\n
        |10.0.0.1|->11:11:11:11:11:11->------->|10.0.0.2|\r\n
        |10.0.0.1|<-------<-22:22:22:22:22:22<-|10.0.0.2|\r\n
        Format:\r\n
        weight_dict['10.0.0.1']['11:11:11:11:11:11'] = 10\r\n
        weight_dict['10.0.0.2']['22:22:22:22:22:22'] = 20\r\n
        """
        def getNeighbor(e, vid):
            return self.graph._vertices[e.v1_id] if e.v2_id == vid else self.graph._vertices[e.v2_id]

        def getWeight(e):
            if weight_dict == None:
                return 1
            else:
                return weight_dict[e.v1_id][v.v2_id]

        # variables
        dist = {}
        prev = {}
        visited = {}
        heap = Heap()

        # init
        src = self.graph._vertices[vid]
        for v in self.graph._vertices.values():
            dist[v] = INFINITY
            visited[v] = False
            prev[v] = None
            heap.add(v, dist[v])
        dist[src] = 0
        heap.ascent(src, dist[src])

        # Dijkstra
        while not heap.isEmpty():
            u:Vertex = heap.poll()
            visited[u] = True
            for interface_id in u.edges.keys():
                if self.use_spanning_tree and self.blocked[u.id][interface_id]: # Spanning Tree Blocked
                    continue
                e_hash_id = u.edges[interface_id]
                e = self.graph._edges[e_hash_id]
                v = getNeighbor(e, u.id)
                if visited[v]:
                    continue
                wl = dist[u] + getWeight(e)
                if dist[v] > wl:
                    dist[v] = wl
                    heap.ascent(v, dist[v])
                    if prev[u]  == None:
                        prev[v] = interface_id
                    else:
                        prev[v] = prev[u]

        rtn = {}
        for v in prev.keys():
            rtn[v.id] = prev[v]
        self.rtn_cache[vid] = rtn
        return rtn

    def queryShortestPath_BFS(self, vid):
        # varaibles
        visited = {}
        last_out_interface = {}

        # init
        q = Queue()
        for v in self.graph._vertices.values():
            visited[v] = False
            last_out_interface[v] = None

        # BFS
        q.enQueue(self.graph._vertices[vid])
        while not q.isEmpty():
            u:Vertex = q.deQueue()
            for interface_id in u.interfaces.keys():
                if self.use_spanning_tree and self.blocked[u.id][interface_id]: # Spanning Tree Blocked
                    continue
                if not self.graph._interface_clear(u.id, interface_id):
                    continue
                next_v_id = self.graph._get_next_vertexid(u.id, interface_id)
                next_v = self.graph._vertices[next_v_id]
                if visited[next_v]:
                    continue
                if last_out_interface[u] == None:
                    last_out_interface[next_v] = interface_id
                else:
                    last_out_interface[next_v] = last_out_interface[u]

                q.enQueue(next_v)
                visited[next_v] = True
        
        rtn = {}
        for v in last_out_interface.keys():
            rtn[v.id] = last_out_interface[v]
        self.rtn_cache[vid] = rtn
        return rtn


