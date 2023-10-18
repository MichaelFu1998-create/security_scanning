def is_node_highlighted(graph: BELGraph, node: BaseEntity) -> bool:
    """Returns if the given node is highlighted.

    :param graph: A BEL graph
    :param node: A BEL node
    :type node: tuple
    :return: Does the node contain highlight information?
    :rtype: bool
    """
    return NODE_HIGHLIGHT in graph.node[node]