def build_source_namespace_filter(namespaces: Strings) -> EdgePredicate:
    """Pass for edges whose source nodes have the given namespace or one of the given namespaces.

    :param namespaces: The namespace or namespaces to filter by
    """
    if isinstance(namespaces, str):
        def source_namespace_filter(_, u: BaseEntity, __, ___) -> bool:
            return node_has_namespace(u, namespaces)

    elif isinstance(namespaces, Iterable):
        namespaces = set(namespaces)

        def source_namespace_filter(_, u: BaseEntity, __, ___) -> bool:
            return node_has_namespaces(u, namespaces)

    else:
        raise TypeError

    return source_namespace_filter