def calculate_concordance(graph: BELGraph, key: str, cutoff: Optional[float] = None,
                          use_ambiguous: bool = False) -> float:
    """Calculates network-wide concordance.

    Assumes data already annotated with given key

    :param graph: A BEL graph
    :param key: The node data dictionary key storing the logFC
    :param cutoff: The optional logFC cutoff for significance
    :param use_ambiguous: Compare to ambiguous edges as well
    """
    correct, incorrect, ambiguous, _ = calculate_concordance_helper(graph, key, cutoff=cutoff)

    try:
        return correct / (correct + incorrect + (ambiguous if use_ambiguous else 0))
    except ZeroDivisionError:
        return -1.0