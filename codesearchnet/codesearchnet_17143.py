def get_namespaces_with_incorrect_names(graph: BELGraph) -> Set[str]:
    """Return the set of all namespaces with incorrect names in the graph."""
    return {
        exc.namespace
        for _, exc, _ in graph.warnings
        if isinstance(exc, (MissingNamespaceNameWarning, MissingNamespaceRegexWarning))
    }