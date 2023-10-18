def get_separate_unstable_correlation_triples(graph: BELGraph) -> Iterable[NodeTriple]:
    """Yield all triples of nodes A, B, C such that ``A pos B``, ``A pos C``, and ``B neg C``.

    :return: An iterator over triples of unstable graphs, where the second two are negative
    """
    cg = get_correlation_graph(graph)

    for a, b, c in get_correlation_triangles(cg):
        if POSITIVE_CORRELATION in cg[a][b] and POSITIVE_CORRELATION in cg[b][c] and NEGATIVE_CORRELATION in \
                cg[a][c]:
            yield b, a, c
        if POSITIVE_CORRELATION in cg[a][b] and NEGATIVE_CORRELATION in cg[b][c] and POSITIVE_CORRELATION in \
                cg[a][c]:
            yield a, b, c
        if NEGATIVE_CORRELATION in cg[a][b] and POSITIVE_CORRELATION in cg[b][c] and POSITIVE_CORRELATION in \
                cg[a][c]:
            yield c, a, b