def get_names_including_errors(graph: BELGraph) -> Mapping[str, Set[str]]:
    """Takes the names from the graph in a given namespace and the erroneous names from the same namespace and returns
    them together as a unioned set

    :return: The dict of the sets of all correct and incorrect names from the given namespace in the graph
    """
    return {
        namespace: get_names_including_errors_by_namespace(graph, namespace)
        for namespace in get_namespaces(graph)
    }