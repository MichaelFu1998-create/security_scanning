def calculate_concordance_probability_by_annotation(graph, annotation, key, cutoff=None, permutations=None,
                                                    percentage=None,
                                                    use_ambiguous=False):
    """Returns the results of concordance analysis on each subgraph, stratified by the given annotation.

    :param pybel.BELGraph graph: A BEL graph
    :param str annotation: The annotation to group by.
    :param str key: The node data dictionary key storing the logFC
    :param float cutoff: The optional logFC cutoff for significance
    :param int permutations: The number of random permutations to test. Defaults to 500
    :param float percentage: The percentage of the graph's edges to maintain. Defaults to 0.9
    :param bool use_ambiguous: Compare to ambiguous edges as well
    :rtype: dict[str,tuple]
    """
    result = [
        (value, calculate_concordance_probability(
            subgraph,
            key,
            cutoff=cutoff,
            permutations=permutations,
            percentage=percentage,
            use_ambiguous=use_ambiguous,
        ))
        for value, subgraph in get_subgraphs_by_annotation(graph, annotation).items()
    ]

    return dict(result)