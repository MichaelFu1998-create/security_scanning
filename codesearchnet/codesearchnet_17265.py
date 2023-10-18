def workflow(
        graph: BELGraph,
        node: BaseEntity,
        key: Optional[str] = None,
        tag: Optional[str] = None,
        default_score: Optional[float] = None,
        runs: Optional[int] = None,
        minimum_nodes: int = 1,
) -> List['Runner']:
    """Generate candidate mechanisms and run the heat diffusion workflow.

    :param graph: A BEL graph
    :param node: The BEL node that is the focus of this analysis
    :param key: The key in the node data dictionary representing the experimental data. Defaults to
     :data:`pybel_tools.constants.WEIGHT`.
    :param tag: The key for the nodes' data dictionaries where the scores will be put. Defaults to 'score'
    :param default_score: The initial score for all nodes. This number can go up or down.
    :param runs: The number of times to run the heat diffusion workflow. Defaults to 100.
    :param minimum_nodes: The minimum number of nodes a sub-graph needs to try running heat diffusion
    :return: A list of runners
    """
    subgraph = generate_mechanism(graph, node, key=key)

    if subgraph.number_of_nodes() <= minimum_nodes:
        return []

    runners = multirun(subgraph, node, key=key, tag=tag, default_score=default_score, runs=runs)
    return list(runners)