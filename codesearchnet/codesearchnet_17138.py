def enrich_reactions(graph: BELGraph):
    """Adds all of the reactants and products of reactions to the graph."""
    nodes = list(get_nodes_by_function(graph, REACTION))
    for u in nodes:
        for v in u.reactants:
            graph.add_has_reactant(u, v)

        for v in u.products:
            graph.add_has_product(u, v)