def calculate_concordance_probability(graph: BELGraph,
                                      key: str,
                                      cutoff: Optional[float] = None,
                                      permutations: Optional[int] = None,
                                      percentage: Optional[float] = None,
                                      use_ambiguous: bool = False,
                                      permute_type: str = 'shuffle_node_data',
                                      ) -> Tuple[float, List[float], float]:
    """Calculates a graph's concordance as well as its statistical probability.



    :param graph: A BEL graph
    :param str key: The node data dictionary key storing the logFC
    :param float cutoff: The optional logFC cutoff for significance
    :param int permutations: The number of random permutations to test. Defaults to 500
    :param float percentage: The percentage of the graph's edges to maintain. Defaults to 0.9
    :param bool use_ambiguous: Compare to ambiguous edges as well
    :returns: A triple of the concordance score, the null distribution, and the p-value.
    """
    if permute_type == 'random_by_edges':
        permute_func = partial(random_by_edges, percentage=percentage)
    elif permute_type == 'shuffle_node_data':
        permute_func = partial(shuffle_node_data, key=key, percentage=percentage)
    elif permute_type == 'shuffle_relations':
        permute_func = partial(shuffle_relations, percentage=percentage)
    else:
        raise ValueError('Invalid permute_type: {}'.format(permute_type))

    graph: BELGraph = graph.copy()
    collapse_to_genes(graph)
    collapse_all_variants(graph)

    score = calculate_concordance(graph, key, cutoff=cutoff)

    distribution = []

    for _ in range(permutations or 500):
        permuted_graph = permute_func(graph)
        permuted_graph_scores = calculate_concordance(permuted_graph, key, cutoff=cutoff, use_ambiguous=use_ambiguous)
        distribution.append(permuted_graph_scores)

    return score, distribution, one_sided(score, distribution)