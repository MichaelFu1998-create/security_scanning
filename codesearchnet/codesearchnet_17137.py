def enrich_composites(graph: BELGraph):
    """Adds all of the members of the composite abundances to the graph."""
    nodes = list(get_nodes_by_function(graph, COMPOSITE))
    for u in nodes:
        for v in u.members:
            graph.add_has_component(u, v)