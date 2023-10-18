def highlight_subgraph(universe: BELGraph, graph: BELGraph):
    """Highlight all nodes/edges in the universe that in the given graph.

    :param universe: The universe of knowledge
    :param graph: The BEL graph to mutate
    """
    highlight_nodes(universe, graph)
    highlight_edges(universe, graph.edges())