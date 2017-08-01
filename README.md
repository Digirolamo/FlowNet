# FlowNet
A python library for simple flow networks. Automatically reduces flow network sizes when multiple sinks and sources are specified. Works with adjacency matrix representations.

Here are a few examples:


    >>> from flownet import FlowNetwork
    
    #  Example 1: creating a flow network via edge ids.
    >>> flow_network = FlowNetwork()
    >>> source_id, sink_id = flow_network.get_source_sink_ids()
    >>> flow_network.add_flow_edge(source_id, "A", 6)
    >>> flow_network.add_flow_edge(source_id, "B", 2)
    >>> flow_network.add_flow_edge("A", "C", 1)
    >>> flow_network.add_flow_edge("B", "C", 2)
    >>> flow_network.add_flow_edge("C", sink_id, 4)
    >>> print(flow_network)
    [[ -,  0,  6,  2,  0], # Source
     [ -,  -,  -,  -,  -], # Sink (0)
     [ 0,  0,  -,  0,  1], # A
     [ 0,  0,  0,  -,  2], # B
     [ 0,  4,  0,  0,  -]] # C

    >>> source = flow_network.get_node(source_id)  # Is also flow_network.source
    >>> source.flow
    8
    >>> list(source.iter_edges())
    [(SuperSource(+), FlowNode(A), 6), (SuperSource(+), FlowNode(B), 2)]

    >>> a_node = flow_network.get_node('A')
    >>> a_node.flow
    1
    >>> list(a_node.iter_edges())
    [(FlowNode(A), FlowNode(C), 1)]

    >>> c_node = flow_network.get_node('C')
    >>> c_node.flow
    4
    >>> list(c_node.iter_edges())
    [(FlowNode(C), SuperSink(-), 4)]

    >>> flow_network.get_maximum_flow()
    3

    #  Examples 2 and 3: creating flow networks from an adjacency matrix.
    >>> adj_matrix = [
        [44, 21, 38, 84, 30, 76, 98, 49],
        [37, 11, 87, 68, 34, 57, 77, 16],
        [58, 46, 55, 17, 49, 29, 69, 26],
        [82, 72, 89, 24, 58, 11, 19, 42],
        [98, 74, 25, 81, 54, 91, 90, 58],
        [15, 48, 24, 19, 12, 76, 68, 28],
        [82, 35, 66, 39, 55, 36, 48, 10],
        [68, 17, 30, 23, 44, 65, 16, 52]
        ]

    >>> sources = [0]
    >>> sinks = [1]
    >>> flow_network = FlowNetwork.from_adjacency_matrix(adj_matrix, sources, sinks)
    >>> print(flow_network)
    [[ - ,  21,  38,  84,  30,  76,  98,  49], # Source
     [ - ,  - ,  - ,  - ,  - ,  - ,  - ,  - ], # Sink (376)
     [ 58,  46,  - ,  17,  49,  29,  69,  26], # 2
     [ 82,  72,  89,  - ,  58,  11,  19,  42], # 3
     [ 98,  74,  25,  81,  - ,  91,  90,  58], # 4
     [ 15,  48,  24,  19,  12,  - ,  68,  28], # 5
     [ 82,  35,  66,  39,  55,  36,  - ,  10], # 6
     [ 68,  17,  30,  23,  44,  65,  16,  - ]] # 7

     >>> flow_network.get_maximum_flow()
    313

    >>> sources = [6, 3, 2]
    >>> sinks = [0, 1]
    >>> flow_network = FlowNetwork.from_adjacency_matrix(adj_matrix, sources, sinks)
    >>> print(flow_network)
    [[ -  ,  375,  162,   76,   78], # Source
     [ -  ,  -  ,  -  ,  -  ,  -  ], # Sink (714)
     [ 196,  172,  -  ,   91,   58], # 4
     [ 111,   63,   12,  -  ,   28], # 5
     [  69,   85,   44,   65,  -  ]] # 7

    >>> flow_network.get_maximum_flow()
    691
