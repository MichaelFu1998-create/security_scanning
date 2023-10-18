def get_undefined_namespaces(graph: BELGraph) -> Set[str]:
    """Get all namespaces that are used in the BEL graph aren't actually defined."""
    return {
        exc.namespace
        for _, exc, _ in graph.warnings
        if isinstance(exc, UndefinedNamespaceWarning)
    }