def get_incorrect_names_by_namespace(graph: BELGraph, namespace: str) -> Set[str]:
    """Return the set of all incorrect names from the given namespace in the graph.

    :return: The set of all incorrect names from the given namespace in the graph
    """
    return {
        exc.name
        for _, exc, _ in graph.warnings
        if isinstance(exc, (MissingNamespaceNameWarning, MissingNamespaceRegexWarning)) and exc.namespace == namespace
    }