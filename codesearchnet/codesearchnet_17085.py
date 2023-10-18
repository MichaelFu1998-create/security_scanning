def highlight_nodes(graph: BELGraph, nodes: Optional[Iterable[BaseEntity]] = None, color: Optional[str]=None):
    """Adds a highlight tag to the given nodes.

    :param graph: A BEL graph
    :param nodes: The nodes to add a highlight tag on
    :param color: The color to highlight (use something that works with CSS)
    """
    color = color or NODE_HIGHLIGHT_DEFAULT_COLOR
    for node in nodes if nodes is not None else graph:
        graph.node[node][NODE_HIGHLIGHT] = color