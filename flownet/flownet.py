"""A simple flow network module.

This module contains the classes and functions written to create, examine,
and solve simple problems on flow networks.

Copyright (C) 2017 Chris Digirolamo

"""
from collections import deque, OrderedDict
from decimal import Decimal
import weakref

INF = Decimal('Infinity')


class FlowNode(object):
    """
    A node with flow network functionality. Automatically
    creates, adjusts, and deletes edges and connects by
    simply using the `add_flow` and `remove_flow` functions.


    Args:
        key (int): A unique identifier for the node.

    Attributes:
        key (int): A unique identifier for the node.

        edge_flow (dict[FlowNode, int]): Maps the flow for this node.
            Stores the flow of children nodes. Basically stores the
            edge.
        parents (set): The parents are the nodes that flow into
            this node.


    """
    def __init__(self, key):
        self._parents = set([])
        self._key = key
        self.edge_flow = OrderedDict()

    @property
    def flow(self):
        """int: The total flow from this FlowNode."""
        return sum(self.edge_flow.itervalues())

    @property
    def key(self):
        """object: The unique node identifier."""
        return self._key

    def add_flow(self, child, amount):
        """
        Adds a a flow from this node to a child node.
        If the edge already exists, adds to it, else
        we create a new edge.

        Args:
            child (FlowNode): The child who receives
                flow from this node.
            amount (int): The amount of flow to add.

        """
        if child is self:
            raise ValueError("Cannot add flow to self.")
        if child not in self.edge_flow:
            self.edge_flow[child] = amount
            child._parents.add(weakref.ref(self))
        else:
            self.edge_flow[child] += amount

    def reduce_flow(self, child, amount=INF):
        """
        Removes flow from an edge. If the flow becomes
        <= 0, the edge is removed.

        Args:
            child (FlowNode): The child node to remove
                flow from.
            amount (int): The amount of flow to remove.
                Defaults to infinity (to guarantees removal
                of the edge)

        """
        if child is self:
            raise ValueError("Cannot remove flow from self.")
        if amount < self.edge_flow[child]:
            self.edge_flow[child] -= amount
        else:
            del self.edge_flow[child]
            child._parents.remove(weakref.ref(self))

    def iter_children(self):
        """Iterate through the nodes that this node flows into.

        Yields:
            FlowNode: Each child of this node.

            """
        for child in self.edge_flow.iterkeys():
            yield child

    def iter_parents(self):
        """Iterate through the nodes that flow into this node.

        Yields:
            FlowNode: Each parents of this node.

            """
        #Stored as weakrefs
        for ref in self._parents:
            parent = ref()
            if parent is not None:
                yield parent

    def iter_edges(self):
        """Iterate through the edges of this node.

        Yields:
            tuple: (parent, child, capacity) of the flow.

        """
        for child, capacity in self.edge_flow.iteritems():
            yield (self, child, capacity)

    def iter_dfs_edges(self):
        """ A depth first search following the flow from this node.

        Note:
            The first node yielded is the calling instance itself.

        Yields:
            tuple[FlowNode]: The next (parent, child) nodes in the search.

        """
        node_queue = deque([(self, c) for c in self.edge_flow.iterkeys()])
        visited = set([c for p, c in node_queue])
        visited.add(self)
        while node_queue:
            parent, child = node_queue.pop()
            yield parent, child
            for granchild in child.edge_flow.iterkeys():
                if granchild not in visited:
                    visited.add(granchild)
                    node_queue.append((child, granchild))

    def __repr__(self):
        cls_name = self.__class__.__name__
        text = "{}({})"
        return text.format(cls_name, self.key)


class SuperSink(FlowNode):
    """The only sink node.

    If there are multiple sinks in a graph, one instance of this node
    can handle them.

    Attributes:
        consumed (int): As a sink, flows are consumed, this
            counts the consumed flow.

    """
    def __init__(self, *args, **kwargs):
        super(SuperSink, self).__init__(*args, **kwargs)
        self.consumed = 0

    @property
    def flow(self):
        """int: The total flow from this node."""
        return INF

    def add_flow(self, child, amount):
        """
        Rather than adding flow from this node to a child node,
        the sink consumes flow.

        Args:
            child (FlowNode): The child who receives
                flow from this node.
            amount (int): The amount of flow to add.


        """
        self.consumed += amount


class SuperSource(FlowNode):
    """The only source node.

    If there are multiple sources in a graph, one instance of this node
    can handle them.

    """


class FlowNetwork(object):
    """
    A class for flow network functionality. Flow networks created with this
    class automatically reduce the network size by using one sink and one
    source.

    Attributes:
        node_key_dict (OrderedDict[key, FlowNode]): The dict of all created
            nodes.

    """
    def __init__(self):
        self._source = SuperSource("+")
        self._sink = SuperSink("-")
        start_d = [(self.source.key, self.source), (self.sink.key, self.sink)]
        self.node_key_dict = OrderedDict(start_d)

    @property
    def source(self):
        """SuperSource: The only source node."""
        return self._source

    @property
    def sink(self):
        """SuperSink: The only sink node."""
        return self._sink

    def get_source_sink_ids(self):
        """Gets the source and sink ids.

        Returns:
            tuple[FlowNode]: The source and sink.

        """
        return self.source.key, self.sink.key

    def get_node(self, node_id):
        """Gets the node from an id.

        Args:
            node_id (str): The unique id of the node.

        Returns:
            FlowNode: The node.

        """
        return self.node_key_dict[node_id]

    def add_flow_edge(self, parent, child, capacity):
        """
        Adds a a flow from a parent node to a child node.
        If the node and edge already exists, adds to it, else
        we create a new node and/or edge.

        Args:
            parent (str): The key of the parent who is sending the
                flow.
            child (str): The key of the child who receives
                flow from this node.
            capacity (int): The max amount of flow to add.

        """
        if isinstance(parent, FlowNode) or isinstance(child, FlowNode):
            raise TypeError("add_flow_edge args are node keys, not nodes themselves.")
        if parent not in self.node_key_dict:
            self.node_key_dict[parent] = FlowNode(parent)
        parent = self.node_key_dict[parent]
        if child not in self.node_key_dict:
            self.node_key_dict[child] = FlowNode(child)
        child = self.node_key_dict[child]
        parent.add_flow(child, capacity)

    def get_maximum_flow(self):
        """Gets the maximum flow from source to sink.

        Returns:
            int: The maximum flow.

        """
        new_copy = self.from_flow_network(self)
        start_consumed = new_copy.sink.consumed
        new_copy.send_max_flow_to_sink()
        return new_copy.sink.consumed - start_consumed

    def send_max_flow_to_sink(self):
        """
        Sends the maximum amount of flow from the source to the sink.

        Partially implements the Ford-Fulkerson maximum flow algorithm
        to solve maximum flow by sending flow using function in this
        FlowNetwork and the FlowNode class.

        You end up finding the maximum flow if you check
        how much the sink consumed.

        """
        parent_map = self._get_dfs_sink_flow_path()
        while parent_map:
            minimum_path_flow = INF
            node = self.sink
            while node is not self.source:
                parent = parent_map[node]
                flow = parent.edge_flow[node]
                minimum_path_flow = min(minimum_path_flow, flow)
                node = parent
            node = self.sink
            while node is not self.source:
                parent = parent_map[node]
                flow = parent.edge_flow[node]
                parent.reduce_flow(node, minimum_path_flow)
                node.add_flow(parent, minimum_path_flow)
                node = parent
            parent_map = self._get_dfs_sink_flow_path()

    def _get_dfs_sink_flow_path(self):
        """A single path from this node to the sink.

        A breadth first search following the flow from
        this node.

        Returns:
            dict[FlowNode, FlowNode]: Each child to parent in
            the path.

        """
        node_path = {}
        for parent, child in self.source.iter_dfs_edges():
            node_path[child] = parent
            if child is self.sink:
                break
        if self.sink not in node_path:
            return dict()
        child = self.sink
        parent = node_path[child]
        exact_path = {child: parent}
        while parent is not self.source:
            child = parent
            parent = node_path[child]
            exact_path[child] = parent
        return exact_path

    def iter_edge_values(self):
        """Iterator of all edges.

        Yields:
            tuple[]: (parent, child, value) for all edges in the
            flow network.

        """
        visited = set()
        for node in self.node_key_dict.values():
            for parent, child in node.iter_dfs_edges():
                edge = (parent, child)
                if edge in visited:
                    continue
                visited.add(edge)
                yield parent, child, parent.edge_flow[child]

    @classmethod
    def from_adjacency_matrix(cls, adjacency_matrix, sources, sinks):
        """Creates a Flow Network from an adjacency matrix.

        Args:
            adjacency_matrix (list[list[int]): The adjacency matrix representation
                of a flow graph.
            sources (list[int]): list of integers denoting indexes of sources.
            sinks (list[int]): list of integers denoting indexes of sinks.

        """
        flow_network = cls()
        key_to_node = {}
        sources = set(sources)
        sinks = set(sinks)
        size = len(adjacency_matrix)
        for node_idx in xrange(size):
            if node_idx in sinks:
                node = flow_network.sink
            elif node_idx in sources:
                node = flow_network.source
            else:
                node = FlowNode(node_idx)
            key_to_node[node_idx] = node
        # Add Flow
        for node_idx in xrange(size):
            row = adjacency_matrix[node_idx]
            node = key_to_node[node_idx]
            for next_node_idx in xrange(size):
                next_node = key_to_node[next_node_idx]
                if node is next_node:
                    continue
                capacity = row[next_node_idx]
                flow_network.add_flow_edge(node.key, next_node.key, capacity)
        return flow_network

    @classmethod
    def from_flow_network(cls, flow_network):
        """Creates a copy of a flow network.

        Args:
            flow_network (FlowNetwork): The instance to copy.

        """
        new_flow_network = cls()
        for parent, child, capacity in flow_network.iter_edge_values():
            new_flow_network.add_flow_edge(parent.key, child.key, capacity)
        return new_flow_network

    def __str__(self):
        max_num = max(e[2] for e in self.iter_edge_values())
        largest_str = len(str(max_num))
        f_temp = " {:" + str(largest_str) + "}"
        all_strings = []
        for node in self.node_key_dict.itervalues():
            node_strings = []
            for node_2 in self.node_key_dict.itervalues():
                if  node_2 is node or node is self.sink:
                    txt = f_temp.format('-')
                elif node_2 not in node.edge_flow:
                    txt = f_temp.format(0)
                else:
                    txt = f_temp.format(node.edge_flow[node_2])
                node_strings.append(txt)
            node_string = ", ".join(node_strings)
            node_string = "[{}], #".format(node_string)
            if node is self.source:
                node_string += " Source"
            elif node is self.sink:
                node_string += " Sink ({})".format(self.sink.consumed)
            else:
                node_string += " {}".format(node.key)
            all_strings.append(node_string)
        if all_strings:
            all_strings[-1] = all_strings[-1].replace("], #", "]] #")
        entire_string = "\n ".join(all_strings)
        entire_string = "[{}".format(entire_string)
        return entire_string
