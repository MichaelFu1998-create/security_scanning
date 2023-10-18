def get_incorrect_names(graph: BELGraph) -> Mapping[str, Set[str]]:
    """Return the dict of the sets of all incorrect names from the given namespace in the graph.

    :return: The set of all incorrect names from the given namespace in the graph
    """
    return {
        namespace: get_incorrect_names_by_namespace(graph, namespace)
        for namespace in get_namespaces(graph)
    }