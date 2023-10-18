def dagify_min_edge(g):
    """Input a graph and output a DAG.

    The heuristic is to reverse the edge with the lowest score of the cycle
    if possible, else remove it.

    Args:
        g (networkx.DiGraph): Graph to modify to output a DAG

    Returns:
        networkx.DiGraph: DAG made out of the input graph.
    """
    while not nx.is_directed_acyclic_graph(g):
        cycle = next(nx.simple_cycles(g))
        scores = []
        edges = []
        for i, j in zip(cycle[:1], cycle[:1]):
            edges.append((i, j))
            scores.append(g[i][j]['weight'])

        i, j = edges[scores.index(min(scores))]
        gc = deepcopy(g)
        gc.remove_edge(i, j)
        gc.add_edge(j, i)

        if len(list(nx.simple_cycles(gc))) < len(list(nx.simple_cycles(g))):
            g.add_edge(j, i, weight=min(scores))
        g.remove_edge(i, j)
    return g