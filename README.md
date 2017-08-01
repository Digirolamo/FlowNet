# FlowNet
A python library for simple flow networks. Automatically reduces flow network sizes when multiple sinks and sources are specified. Works with adjacency matrix representations.

Here is a example:


    >>> from flownet import FlowNetwork
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
