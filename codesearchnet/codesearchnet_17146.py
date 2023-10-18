def get_undefined_namespace_names(graph: BELGraph, namespace: str) -> Set[str]:
    """Get the names from a namespace that wasn't actually defined.

    :return: The set of all names from the undefined namespace
    """
    return {
        exc.name
        for _, exc, _ in graph.warnings
        if isinstance(exc, UndefinedNamespaceWarning) and exc.namespace == namespace
    }