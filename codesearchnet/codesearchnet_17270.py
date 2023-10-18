def calculate_average_score_by_annotation(
        graph: BELGraph,
        annotation: str,
        key: Optional[str] = None,
        runs: Optional[int] = None,
        use_tqdm: bool = False,
) -> Mapping[str, float]:
    """For each sub-graph induced over the edges matching the annotation, calculate the average score
    for all of the contained biological processes

    Assumes you haven't done anything yet

    1. Generates biological process upstream candidate mechanistic sub-graphs with
       :func:`generate_bioprocess_mechanisms`
    2. Calculates scores for each sub-graph with :func:`calculate_average_scores_on_sub-graphs`
    3. Overlays data with pbt.integration.overlay_data
    4. Calculates averages with pbt.selection.group_nodes.average_node_annotation

    :param graph: A BEL graph
    :param annotation: A BEL annotation
    :param key: The key in the node data dictionary representing the experimental data. Defaults to
     :data:`pybel_tools.constants.WEIGHT`.
    :param runs: The number of times to run the heat diffusion workflow. Defaults to 100.
    :param use_tqdm: Should there be a progress bar for runners?
    :return: A dictionary from {str annotation value: tuple scores}

    Example Usage:

    >>> import pybel
    >>> from pybel_tools.integration import overlay_data
    >>> from pybel_tools.analysis.heat import calculate_average_score_by_annotation
    >>> graph = pybel.from_path(...)
    >>> scores = calculate_average_score_by_annotation(graph, 'subgraph')
    """
    candidate_mechanisms = generate_bioprocess_mechanisms(graph, key=key)

    #: {bp tuple: list of scores}
    scores: Mapping[BaseEntity, Tuple] = calculate_average_scores_on_subgraphs(
        subgraphs=candidate_mechanisms,
        key=key,
        runs=runs,
        use_tqdm=use_tqdm,
    )

    subgraph_bp: Mapping[str, List[BaseEntity]] = defaultdict(list)
    subgraphs: Mapping[str, BELGraph] = get_subgraphs_by_annotation(graph, annotation)
    for annotation_value, subgraph in subgraphs.items():
        subgraph_bp[annotation_value].extend(get_nodes_by_function(subgraph, BIOPROCESS))

    #: Pick the average by slicing with 0. Refer to :func:`calculate_average_score_on_subgraphs`
    return {
        annotation_value: np.average(scores[bp][0] for bp in bps)
        for annotation_value, bps in subgraph_bp.items()
    }