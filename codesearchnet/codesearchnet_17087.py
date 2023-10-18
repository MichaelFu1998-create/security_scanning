def remove_highlight_nodes(graph: BELGraph, nodes: Optional[Iterable[BaseEntity]]=None) -> None:
    """Removes the highlight from the given nodes, or all nodes if none given.

    :param graph: A BEL graph
    :param nodes: The list of nodes to un-highlight
    """
    for node in graph if nodes is None else nodes:
        if is_node_highlighted(graph, node):
            del graph.node[node][NODE_HIGHLIGHT]