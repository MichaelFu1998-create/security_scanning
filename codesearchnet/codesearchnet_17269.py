def workflow_all_aggregate(graph: BELGraph,
                           key: Optional[str] = None,
                           tag: Optional[str] = None,
                           default_score: Optional[float] = None,
                           runs: Optional[int] = None,
                           aggregator: Optional[Callable[[Iterable[float]], float]] = None,
                           ):
    """Run the heat diffusion workflow to get average score for every possible candidate mechanism.

    1. Get all biological processes
    2. Get candidate mechanism induced two level back from each biological process
    3. Heat diffusion workflow on each candidate mechanism for multiple runs
    4. Report average scores for each candidate mechanism

    :param graph: A BEL graph
    :param key: The key in the node data dictionary representing the experimental data. Defaults to
     :data:`pybel_tools.constants.WEIGHT`.
    :param tag: The key for the nodes' data dictionaries where the scores will be put. Defaults to 'score'
    :param default_score: The initial score for all nodes. This number can go up or down.
    :param runs: The number of times to run the heat diffusion workflow. Defaults to 100.
    :param aggregator: A function that aggregates a list of scores. Defaults to :func:`numpy.average`.
                       Could also use: :func:`numpy.mean`, :func:`numpy.median`, :func:`numpy.min`, :func:`numpy.max`
    :return: A dictionary of {node: upstream causal subgraph}
    """
    results = {}

    bioprocess_nodes = list(get_nodes_by_function(graph, BIOPROCESS))

    for bioprocess_node in tqdm(bioprocess_nodes):
        subgraph = generate_mechanism(graph, bioprocess_node, key=key)

        try:
            results[bioprocess_node] = workflow_aggregate(
                graph=subgraph,
                node=bioprocess_node,
                key=key,
                tag=tag,
                default_score=default_score,
                runs=runs,
                aggregator=aggregator
            )
        except Exception:
            log.exception('could not run on %', bioprocess_node)

    return results