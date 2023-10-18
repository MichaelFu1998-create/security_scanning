def get_regulatory_pairs(graph: BELGraph) -> Set[NodePair]:
    """Find pairs of nodes that have mutual causal edges that are regulating each other such that ``A -> B`` and
    ``B -| A``.

    :return: A set of pairs of nodes with mutual causal edges
    """
    cg = get_causal_subgraph(graph)

    results = set()

    for u, v, d in cg.edges(data=True):
        if d[RELATION] not in CAUSAL_INCREASE_RELATIONS:
            continue

        if cg.has_edge(v, u) and any(dd[RELATION] in CAUSAL_DECREASE_RELATIONS for dd in cg[v][u].values()):
            results.add((u, v))

    return results