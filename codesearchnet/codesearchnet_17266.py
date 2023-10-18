def multirun(graph: BELGraph,
             node: BaseEntity,
             key: Optional[str] = None,
             tag: Optional[str] = None,
             default_score: Optional[float] = None,
             runs: Optional[int] = None,
             use_tqdm: bool = False,
             ) -> Iterable['Runner']:
    """Run the heat diffusion workflow multiple times, each time yielding a :class:`Runner` object upon completion.

    :param graph: A BEL graph
    :param node: The BEL node that is the focus of this analysis
    :param key: The key in the node data dictionary representing the experimental data. Defaults to
     :data:`pybel_tools.constants.WEIGHT`.
    :param tag: The key for the nodes' data dictionaries where the scores will be put. Defaults to 'score'
    :param default_score: The initial score for all nodes. This number can go up or down.
    :param runs: The number of times to run the heat diffusion workflow. Defaults to 100.
    :param use_tqdm: Should there be a progress bar for runners?
    :return: An iterable over the runners after each iteration
    """
    if runs is None:
        runs = 100

    it = range(runs)

    if use_tqdm:
        it = tqdm(it, total=runs)

    for i in it:
        try:
            runner = Runner(graph, node, key=key, tag=tag, default_score=default_score)
            runner.run()
            yield runner
        except Exception:
            log.debug('Run %s failed for %s', i, node)