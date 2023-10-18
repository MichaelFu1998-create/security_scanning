def get_largest_component(graph: BELGraph) -> BELGraph:
    """Get the giant component of a graph."""
    biggest_component_nodes = max(nx.weakly_connected_components(graph), key=len)
    return subgraph(graph, biggest_component_nodes)