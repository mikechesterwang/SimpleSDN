from Graph import *

def test_dij():
    graph:Graph = Graph()
    graph.addVertex('s1', ['->h1', '->s2', '->s3'])
    graph.addVertex('s2', ['->h2', '->s1', '->s3'])
    graph.addVertex('s3', ['->h3', '->s1', '->s2'])
    graph.addVertex('h1', ['->s1'])
    graph.addVertex('h2', ['->s2'])
    graph.addVertex('h3', ['->s3'])

    graph.addEdge('h1', 's1', '->s1', '->h1')
    graph.addEdge('h2', 's2', '->s2', '->h2')
    graph.addEdge('h3', 's3', '->s3', '->h3')
    graph.addEdge('s1', 's2', '->s2', '->s1')
    graph.addEdge('s2', 's3', '->s3', '->s2')
    graph.addEdge('s3', 's1', '->s1', '->s3')
    print("===================s1====================")
    h1_dict = graph.rs.queryShortestPath_Dijkstra('s1')
    for vid in h1_dict:
        print(vid, h1_dict[vid])

    print("===================s2====================")
    h1_dict = graph.rs.queryShortestPath_Dijkstra('s2')
    for vid in h1_dict:
        print(vid, h1_dict[vid])
    print("===================s3====================")
    h1_dict = graph.rs.queryShortestPath_Dijkstra('s3')
    for vid in h1_dict:
        print(vid, h1_dict[vid])

    print("===================h1====================")
    h1_dict = graph.rs.queryShortestPath_Dijkstra('h1')
    for vid in h1_dict:
        print(vid, h1_dict[vid])

    print("===================h2====================")
    h1_dict = graph.rs.queryShortestPath_Dijkstra('h2')
    for vid in h1_dict:
        print(vid, h1_dict[vid])


    print("===================h3====================")
    h1_dict = graph.rs.queryShortestPath_Dijkstra('h3')
    for vid in h1_dict:
        print(vid, h1_dict[vid])


    print(graph.print_path('h1', 'h2'))
    print(graph.print_path('h2', 'h3'))
    print(graph.print_path('h3', 'h1'))

def test_print_path():
    graph:Graph = Graph()
    graph.addVertex('s1', ['->h1', '->s2', '->s3'])
    graph.addVertex('s2', ['->h2', '->s1', '->s3'])
    graph.addVertex('s3', ['->h3', '->s1', '->s2'])
    graph.addVertex('h1', ['->s1'])
    graph.addVertex('h2', ['->s2'])
    graph.addVertex('h3', ['->s3'])
    graph.addEdge('h1', 's1', '->s1', '->h1')
    graph.addEdge('h2', 's2', '->s2', '->h2')
    graph.addEdge('h3', 's3', '->s3', '->h3')
    graph.addEdge('s1', 's2', '->s2', '->s1')
    graph.addEdge('s2', 's3', '->s3', '->s2')
    graph.addEdge('s3', 's1', '->s1', '->s3')
    graph.queryShortestPath('s1')
    graph.queryShortestPath('s2')
    graph.queryShortestPath('s3')
    graph.queryShortestPath('h1')
    graph.queryShortestPath('h2')
    graph.queryShortestPath('h3')
    print(graph.print_topology())
    print()
    print(graph.print_path('h1', 'h2'))
    print(graph.print_path('h1', 'h3'))
    print()
    print(graph.print_path('h2', 'h1'))
    print(graph.print_path('h2', 'h3'))
    print()
    print(graph.print_path('h3', 'h1'))
    print(graph.print_path('h3', 'h2')) 

def test_case_mst():
    graph:Graph = Graph()
    graph.addVertex('s1', ['->h1', '->s2', '->s3'])
    graph.addVertex('s2', ['->h2', '->s1', '->s3'])
    graph.addVertex('s3', ['->h3', '->s1', '->s2'])
    graph.addVertex('h1', ['->s1'])
    graph.addVertex('h2', ['->s2'])
    graph.addVertex('h3', ['->s3'])
    graph.addEdge('h1', 's1', '->s1', '->h1')
    graph.addEdge('h2', 's2', '->s2', '->h2')
    graph.addEdge('h3', 's3', '->s3', '->h3')
    graph.addEdge('s1', 's2', '->s2', '->s1')
    graph.addEdge('s2', 's3', '->s3', '->s2')
    graph.addEdge('s3', 's1', '->s1', '->s3')

    graph.rs.use_spanning_tree = True
    graph.rs.updateSpanningTree_BFS('s1')

    print("spanning tree")
    for vid in graph._vertices.keys():
            for iid in graph._vertices[vid].interfaces.keys():
                print( vid, iid, "blocked" if graph.rs.blocked[vid][iid] else "connecting")

    print('BFS query example')
    sw_ft_dict = graph.queryShortestPath('s1')
    sw_ft_dict = graph.queryShortestPath('s2')
    sw_ft_dict = graph.queryShortestPath('s3')
    sw_ft_dict = graph.queryShortestPath('h1')
    sw_ft_dict = graph.queryShortestPath('h2')
    sw_ft_dict = graph.queryShortestPath('h3')
    print(graph.print_topology())
    print(graph.print_spanning_tree())
 
def test_case_1():
    graph:Graph = Graph()
    graph.addVertex('s1', ['->h1', '->s2', '->s3'])
    graph.addVertex('s2', ['->h2', '->s1', '->s3'])
    graph.addVertex('s3', ['->h3', '->s1', '->s2'])
    graph.addVertex('h1', ['->s1'])
    graph.addVertex('h2', ['->s2'])
    graph.addVertex('h3', ['->s3'])
    graph.addEdge('h1', 's1', '->s1', '->h1')
    graph.addEdge('h2', 's2', '->s2', '->h2')
    graph.addEdge('h3', 's3', '->s3', '->h3')
    graph.addEdge('s1', 's2', '->s2', '->s1')
    graph.addEdge('s2', 's3', '->s3', '->s2')
    graph.addEdge('s3', 's1', '->s1', '->s3')
    print('BFS query example')
    sw_ft_dict = graph.queryShortestPath('s1')
    print("s1 Flow table dictionary")
    for v in sw_ft_dict.keys():
        print("\t", v, ':', sw_ft_dict[v])
    sw_ft_dict = graph.queryShortestPath('s2')
    print("s2 Flow table dictionary")
    for v in sw_ft_dict.keys():
        print("\t", v, ':', sw_ft_dict[v])
    sw_ft_dict = graph.queryShortestPath('s3')
    print("s3 Flow table dictionary")
    for v in sw_ft_dict.keys():
        print("\t", v, ':', sw_ft_dict[v])
    
def test_case_2():
    graph:Graph = Graph()
    # 添加三个swicth
    graph.addVertex('switch0/1', ['00:00:ff:ff:ff:ff', '00:01:ff:ff:ff:ff', '00:02:ff:ff:ff:ff', '00:03:ff:ff:ff:ff'])
    switch1 = graph._vertices['switch0/1']
    graph.addVertex('switch0/2', ['00:00:ee:ee:ee:ee', '00:01:ee:ee:ee:ee', '00:02:ee:ee:ee:ee'])
    switch2 = graph._vertices['switch0/2']
    graph.addVertex('switch0/3', ['00:00:dd:dd:dd:dd', '00:01:dd:dd:dd:dd', '00:02:dd:dd:dd:dd'])
    switch3 = graph._vertices['switch0/3']

    # 添加四个host
    graph.addVertex('10.0.0.2', ['00:00:00:00:00:00'])
    host1 = graph._vertices['10.0.0.2']

    graph.addVertex('10.0.0.3', ['00:00:00:00:00:00'])
    host2 = graph._vertices['10.0.0.3']

    graph.addVertex('10.0.0.4', ['00:00:00:00:00:00'])
    host3 = graph._vertices['10.0.0.4']

    graph.addVertex('10.0.0.5', ['00:00:00:00:00:00'])
    host4 = graph._vertices['10.0.0.5']

    # 连接这个switch和host
    graph.addEdge(switch1.id, host1.id, '00:00:ff:ff:ff:ff', '00:00:00:00:00:00')
    graph.addEdge(switch1.id, host3.id, '00:02:ff:ff:ff:ff', '00:00:00:00:00:00')
    graph.addEdge(switch1.id, switch2.id, '00:01:ff:ff:ff:ff', '00:02:ee:ee:ee:ee')
    graph.addEdge(switch2.id, host2.id, '00:02:ee:ee:ee:ee', '00:00:00:00:00:00')
    graph.addEdge(switch1.id, switch3.id, '00:03:ff:ff:ff:ff', '00:00:dd:dd:dd:dd')
    graph.addEdge(switch2.id, switch3.id, '00:00:ee:ee:ee:ee', '00:01:dd:dd:dd:dd')
    graph.addEdge(switch3.id, host4.id, '00:02:dd:dd:dd:dd', '00:00:00:00:00:00')
    

    """
                                             10.0.0.3                                              10.0.0.5
                                            ---------                                             --------- 
                                            | host2 |                                             | host4 |
                                            ---------                                             ---------      
                                                | 00:00:00:00:00:00                                   | 00:00:00:00:00:00
                                                50                                                    |
                                                | 00:02:ee:ee:ee:ee                                   20
                                                |                                                     | 00:02:dd:dd:dd:dd
                                          =============== 00:00:ee:ee:ee:ee  00:01:dd:dd:dd:dd ===============
                                          || Switch0/2 ||----------------10--------------------|| Switch0/3 ||
                                          ===============                                      ===============
                              00:01:ee:ee:ee:ee |                               ----------------------| 00:00:dd:dd:dd:dd 
                                               99                               |
    10.0.0.2                  00:01:ff:ff:ff:ff |                               |      
    --------- 00:00:00:00:00:00           =============== 00:03:ff:ff:ff:ff     |     ---------
    | host1 |--------------10-------------|| Swicth0/1 ||-----------20-----------     | host3 | 10.0.0.4
    ---------           00:00:ff:ff:ff:ff ===============                             ---------
                                                | 00:02:ff:ff:ff:ff     00:00:00:00:00:00 |
                                                10                                        |
                                                -------------------------------------------

    """
    print('BFS query example')
    sw_ft_dict = graph.queryShortestPath('switch0/1')
    print("switch0/1 Flow table dictionary")
    for v in sw_ft_dict.keys():
        print("\t", v, ':', sw_ft_dict[v])
    sw_ft_dict = graph.queryShortestPath('switch0/2')
    print("switch0/2 Flow table dictionary")
    for v in sw_ft_dict.keys():
        print("\t", v, ':', sw_ft_dict[v])
    sw_ft_dict = graph.queryShortestPath('switch0/3')
    print("switch0/3 Flow table dictionary")
    for v in sw_ft_dict.keys():
        print("\t", v, ':', sw_ft_dict[v])
    
    print(' ')

    print('Dijkstra query example')
    weight_dict = {
        '10.0.0.2':{
            '00:00:00:00:00:00':10
        },
        'switch0/1':{
            '00:00:ff:ff:ff:ff':10,
            '00:01:ff:ff:ff:ff':99,
            '00:02:ff:ff:ff:ff':10,
            '00:03:ff:ff:ff:ff':20
        },
        '10.0.0.4':{
            '00:00:00:00:00:00':10
        },
        'switch0/3':{
            '00:00:dd:dd:dd:dd':20,
            '00:01:dd:dd:dd:dd':10,
            '00:02:dd:dd:dd:dd':20
        },
        'switch0/2':{
            '00:00:ee:ee:ee:ee':10,
            '00:01:ee:ee:ee:ee':99,
            '00:02:ee:ee:ee:ee':50,
        },
        '10.0.0.3':{
            '00:00:00:00:00:00':50
        },
        '10.0.0.4':{
            '00:00:00:00:00:00':20
        }
    }
    dist, sw_ft_dict = graph.queryShortestPath('switch0/1', 'Dijkstra', weight_dict)
    
    print("Distance dictionary")
    for v in dist.keys():
        print("\t", v, ':', dist[v])
    print("Flow table dictionary")
    for v in sw_ft_dict.keys():
        print("\t", v, ':', sw_ft_dict[v])

if __name__ == "__main__":
    test_dij()
