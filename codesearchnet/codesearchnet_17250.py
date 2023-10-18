def calculate_concordance_helper(graph: BELGraph,
                                 key: str,
                                 cutoff: Optional[float] = None,
                                 ) -> Tuple[int, int, int, int]:
    """Help calculate network-wide concordance

    Assumes data already annotated with given key

    :param graph: A BEL graph
    :param key: The node data dictionary key storing the logFC
    :param cutoff: The optional logFC cutoff for significance
    """
    scores = defaultdict(int)

    for u, v, k, d in graph.edges(keys=True, data=True):
        c = edge_concords(graph, u, v, k, d, key, cutoff=cutoff)
        scores[c] += 1

    return (
        scores[Concordance.correct],
        scores[Concordance.incorrect],
        scores[Concordance.ambiguous],
        scores[Concordance.unassigned],
    )