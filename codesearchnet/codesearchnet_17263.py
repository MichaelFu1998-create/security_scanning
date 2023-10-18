def calculate_average_scores_on_graph(
        graph: BELGraph,
        key: Optional[str] = None,
        tag: Optional[str] = None,
        default_score: Optional[float] = None,
        runs: Optional[int] = None,
        use_tqdm: bool = False,
):
    """Calculate the scores over all biological processes in the sub-graph.

    As an implementation, it simply computes the sub-graphs then calls :func:`calculate_average_scores_on_subgraphs` as
    described in that function's documentation.

    :param graph: A BEL graph with heats already on the nodes
    :param key: The key in the node data dictionary representing the experimental data. Defaults to
     :data:`pybel_tools.constants.WEIGHT`.
    :param tag: The key for the nodes' data dictionaries where the scores will be put. Defaults to 'score'
    :param default_score: The initial score for all nodes. This number can go up or down.
    :param runs: The number of times to run the heat diffusion workflow. Defaults to 100.
    :param use_tqdm: Should there be a progress bar for runners?
    :return: A dictionary of {pybel node tuple: results tuple}
    :rtype: dict[tuple, tuple]

    Suggested usage with :mod:`pandas`:

    >>> import pandas as pd
    >>> from pybel_tools.analysis.heat import calculate_average_scores_on_graph
    >>> graph = ...  # load graph and data
    >>> scores = calculate_average_scores_on_graph(graph)
    >>> pd.DataFrame.from_items(scores.items(), orient='index', columns=RESULT_LABELS)

    """
    subgraphs = generate_bioprocess_mechanisms(graph, key=key)
    scores = calculate_average_scores_on_subgraphs(
        subgraphs,
        key=key,
        tag=tag,
        default_score=default_score,
        runs=runs,
        use_tqdm=use_tqdm
    )
    return scores