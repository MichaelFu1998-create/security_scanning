def enrich_complexes(graph: BELGraph) -> None:
    """Add all of the members of the complex abundances to the graph."""
    nodes = list(get_nodes_by_function(graph, COMPLEX))
    for u in nodes:
        for v in u.members:
            graph.add_has_component(u, v)