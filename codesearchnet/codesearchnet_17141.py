def expand_internal(universe: BELGraph, graph: BELGraph, edge_predicates: EdgePredicates = None) -> None:
    """Edges between entities in the sub-graph that pass the given filters.

    :param universe: The full graph
    :param graph: A sub-graph to find the upstream information
    :param edge_predicates: Optional list of edge filter functions (graph, node, node, key, data) -> bool
    """
    edge_filter = and_edge_predicates(edge_predicates)

    for u, v in itt.product(graph, repeat=2):
        if graph.has_edge(u, v) or not universe.has_edge(u, v):
            continue

        rs = defaultdict(list)
        for key, data in universe[u][v].items():
            if not edge_filter(universe, u, v, key):
                continue

            rs[data[RELATION]].append((key, data))

        if 1 == len(rs):
            relation = list(rs)[0]
            for key, data in rs[relation]:
                graph.add_edge(u, v, key=key, **data)
        else:
            log.debug('Multiple relationship types found between %s and %s', u, v)