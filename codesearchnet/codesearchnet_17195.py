def average_node_annotation(graph: BELGraph,
                            key: str,
                            annotation: str = 'Subgraph',
                            aggregator: Optional[Callable[[Iterable[X]], X]] = None,
                            ) -> Mapping[str, X]:
    """Groups graph into subgraphs and assigns each subgraph a score based on the average of all nodes values
    for the given node key

    :param pybel.BELGraph graph: A BEL graph
    :param key: The key in the node data dictionary representing the experimental data
    :param annotation: A BEL annotation to use to group nodes
    :param aggregator: A function from list of values -> aggregate value. Defaults to taking the average of a list of
                       floats.
    :type aggregator: lambda
    """

    if aggregator is None:
        def aggregator(x):
            """Calculates the average"""
            return sum(x) / len(x)

    result = {}

    for subgraph, nodes in group_nodes_by_annotation(graph, annotation).items():
        values = [graph.nodes[node][key] for node in nodes if key in graph.nodes[node]]
        result[subgraph] = aggregator(values)

    return result