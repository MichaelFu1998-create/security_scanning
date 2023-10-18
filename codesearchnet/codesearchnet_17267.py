def workflow_aggregate(graph: BELGraph,
                       node: BaseEntity,
                       key: Optional[str] = None,
                       tag: Optional[str] = None,
                       default_score: Optional[float] = None,
                       runs: Optional[int] = None,
                       aggregator: Optional[Callable[[Iterable[float]], float]] = None,
                       ) -> Optional[float]:
    """Get the average score over multiple runs.

    This function is very simple, and can be copied to do more interesting statistics over the :class:`Runner`
    instances. To iterate over the runners themselves, see :func:`workflow`

    :param graph: A BEL graph
    :param node: The BEL node that is the focus of this analysis
    :param key: The key in the node data dictionary representing the experimental data. Defaults to
     :data:`pybel_tools.constants.WEIGHT`.
    :param tag: The key for the nodes' data dictionaries where the scores will be put. Defaults to 'score'
    :param default_score: The initial score for all nodes. This number can go up or down.
    :param runs: The number of times to run the heat diffusion workflow. Defaults to 100.
    :param aggregator: A function that aggregates a list of scores. Defaults to :func:`numpy.average`.
                       Could also use: :func:`numpy.mean`, :func:`numpy.median`, :func:`numpy.min`, :func:`numpy.max`
    :return: The average score for the target node
    """
    runners = workflow(graph, node, key=key, tag=tag, default_score=default_score, runs=runs)
    scores = [runner.get_final_score() for runner in runners]

    if not scores:
        log.warning('Unable to run the heat diffusion workflow for %s', node)
        return

    if aggregator is None:
        return np.average(scores)

    return aggregator(scores)