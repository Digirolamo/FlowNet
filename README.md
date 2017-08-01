# FlowNet
A python library for simple flow networks. Automatically reduces the network size when multiple sinks and sources are used.

Here is a example:


    >>> from flownet import FlowNetwork
    >>> sources = [0]
    >>> sinks = [1]
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
    >>> flow_network = FlowNetwork.from_adjacency_matrix(adj_matrix, sources, sinks)
    >>> print(flow_network)
    [[ 44,  21,  38,  84,  30,  76,  98,  49] Source,
     [ - ,  - ,  - ,  - ,  - ,  - ,  - ,  - ] Sink (387),
     [ 58,  46,  55,  17,  49,  29,  69,  26] 2,
     [ 82,  72,  89,  24,  58,  11,  19,  42] 3,
     [ 98,  74,  25,  81,  54,  91,  90,  58] 4,
     [ 15,  48,  24,  19,  12,  76,  68,  28] 5,
     [ 82,  35,  66,  39,  55,  36,  48,  10] 6,
     [ 68,  17,  30,  23,  44,  65,  16,  52] 7]
     >>> print(flow_network.get_maximum_flow())
    313

    >>> sources = [6, 3, 2]
    >>> sinks = [0, 1]
    >>> flow_network = FlowNetwork.from_adjacency_matrix(adj_matrix, sources, sinks)
    >>> print(flow_network)
    [[ 426,  375,  162,   76,   78] Source,
     [ -  ,  -  ,  -  ,  -  ,  -  ] Sink (827),
     [ 196,  172,   54,   91,   58] 4,
     [ 111,   63,   12,   76,   28] 5,
     [  69,   85,   44,   65,   52] 7]
    >>> print(flow_network.get_maximum_flow())
    691
