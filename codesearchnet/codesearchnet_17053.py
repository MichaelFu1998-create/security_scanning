def get_chaotic_pairs(graph: BELGraph) -> SetOfNodePairs:
    """Find pairs of nodes that have mutual causal edges that are increasing each other such that ``A -> B`` and
    ``B -> A``.

    :return: A set of pairs of nodes with mutual causal edges
    """
    cg = get_causal_subgraph(graph)

    results = set()

    for u, v, d in cg.edges(data=True):
        if d[RELATION] not in CAUSAL_INCREASE_RELATIONS:
            continue

        if cg.has_edge(v, u) and any(dd[RELATION] in CAUSAL_INCREASE_RELATIONS for dd in cg[v][u].values()):
            results.add(tuple(sorted([u, v], key=str)))

    return results