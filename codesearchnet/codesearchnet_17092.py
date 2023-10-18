def remove_highlight_subgraph(graph: BELGraph, subgraph: BELGraph):
    """Remove the highlight from all nodes/edges in the graph that are in the subgraph.

    :param graph: The BEL graph to mutate
    :param subgraph: The subgraph from which to remove the highlighting
    """
    remove_highlight_nodes(graph, subgraph.nodes())
    remove_highlight_edges(graph, subgraph.edges())