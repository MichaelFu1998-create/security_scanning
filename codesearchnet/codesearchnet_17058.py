def get_mutually_unstable_correlation_triples(graph: BELGraph) -> Iterable[NodeTriple]:
    """Yield triples of nodes (A, B, C) such that ``A neg B``, ``B neg C``, and ``C neg A``."""
    cg = get_correlation_graph(graph)

    for a, b, c in get_correlation_triangles(cg):
        if all(NEGATIVE_CORRELATION in x for x in (cg[a][b], cg[b][c], cg[a][c])):
            yield a, b, c