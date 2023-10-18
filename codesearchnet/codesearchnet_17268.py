def workflow_all(graph: BELGraph,
                 key: Optional[str] = None,
                 tag: Optional[str] = None,
                 default_score: Optional[float] = None,
                 runs: Optional[int] = None,
                 ) -> Mapping[BaseEntity, List[Runner]]:
    """Run the heat diffusion workflow and get runners for every possible candidate mechanism

    1. Get all biological processes
    2. Get candidate mechanism induced two level back from each biological process
    3. Heat diffusion workflow for each candidate mechanism for multiple runs
    4. Return all runner results

    :param graph: A BEL graph
    :param key: The key in the node data dictionary representing the experimental data. Defaults to
     :data:`pybel_tools.constants.WEIGHT`.
    :param tag: The key for the nodes' data dictionaries where the scores will be put. Defaults to 'score'
    :param default_score: The initial score for all nodes. This number can go up or down.
    :param runs: The number of times to run the heat diffusion workflow. Defaults to 100.
    :return: A dictionary of {node: list of runners}
    """
    results = {}

    for node in get_nodes_by_function(graph, BIOPROCESS):
        results[node] = workflow(graph, node, key=key, tag=tag, default_score=default_score, runs=runs)

    return results