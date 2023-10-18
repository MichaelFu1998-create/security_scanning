def node_is_upstream_leaf(graph: BELGraph, node: BaseEntity) -> bool:
    """Return if the node is an upstream leaf.

    An upstream leaf is defined as a node that has no in-edges, and exactly 1 out-edge.
    """
    return 0 == len(graph.predecessors(node)) and 1 == len(graph.successors(node))