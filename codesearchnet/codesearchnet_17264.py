def calculate_average_scores_on_subgraphs(
        subgraphs: Mapping[H, BELGraph],
        key: Optional[str] = None,
        tag: Optional[str] = None,
        default_score: Optional[float] = None,
        runs: Optional[int] = None,
        use_tqdm: bool = False,
        tqdm_kwargs: Optional[Mapping[str, Any]] = None,
) -> Mapping[H, Tuple[float, float, float, float, int, int]]:
    """Calculate the scores over precomputed candidate mechanisms.

    :param subgraphs: A dictionary of keys to their corresponding subgraphs
    :param key: The key in the node data dictionary representing the experimental data. Defaults to
     :data:`pybel_tools.constants.WEIGHT`.
    :param tag: The key for the nodes' data dictionaries where the scores will be put. Defaults to 'score'
    :param default_score: The initial score for all nodes. This number can go up or down.
    :param runs: The number of times to run the heat diffusion workflow. Defaults to 100.
    :param use_tqdm: Should there be a progress bar for runners?
    :return: A dictionary of keys to results tuples

    Example Usage:

    >>> import pandas as pd
    >>> from pybel_tools.generation import generate_bioprocess_mechanisms
    >>> from pybel_tools.analysis.heat import calculate_average_scores_on_subgraphs
    >>> # load graph and data
    >>> graph = ...
    >>> candidate_mechanisms = generate_bioprocess_mechanisms(graph)
    >>> scores = calculate_average_scores_on_subgraphs(candidate_mechanisms)
    >>> pd.DataFrame.from_items(scores.items(), orient='index', columns=RESULT_LABELS)
    """
    results = {}

    log.info('calculating results for %d candidate mechanisms using %d permutations', len(subgraphs), runs)

    it = subgraphs.items()

    if use_tqdm:
        _tqdm_kwargs = dict(total=len(subgraphs), desc='Candidate mechanisms')
        if tqdm_kwargs:
            _tqdm_kwargs.update(tqdm_kwargs)
        it = tqdm(it, **_tqdm_kwargs)

    for node, subgraph in it:
        number_first_neighbors = subgraph.in_degree(node)
        number_first_neighbors = 0 if isinstance(number_first_neighbors, dict) else number_first_neighbors
        mechanism_size = subgraph.number_of_nodes()

        runners = workflow(subgraph, node, key=key, tag=tag, default_score=default_score, runs=runs)
        scores = [runner.get_final_score() for runner in runners]

        if 0 == len(scores):
            results[node] = (
                None,
                None,
                None,
                None,
                number_first_neighbors,
                mechanism_size,
            )
            continue

        scores = np.array(scores)

        average_score = np.average(scores)
        score_std = np.std(scores)
        med_score = np.median(scores)
        chi_2_stat, norm_p = stats.normaltest(scores)

        results[node] = (
            average_score,
            score_std,
            norm_p,
            med_score,
            number_first_neighbors,
            mechanism_size,
        )

    return results