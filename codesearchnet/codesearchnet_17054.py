def get_correlation_graph(graph: BELGraph) -> Graph:
    """Extract an undirected graph of only correlative relationships."""
    result = Graph()

    for u, v, d in graph.edges(data=True):
        if d[RELATION] not in CORRELATIVE_RELATIONS:
            continue

        if not result.has_edge(u, v):
            result.add_edge(u, v, **{d[RELATION]: True})

        elif d[RELATION] not in result[u][v]:
            log.log(5, 'broken correlation relation for %s, %s', u, v)
            result[u][v][d[RELATION]] = True
            result[v][u][d[RELATION]] = True

    return result