def build_target_namespace_filter(namespaces: Strings) -> EdgePredicate:
    """Only passes for edges whose target nodes have the given namespace or one of the given namespaces

    :param namespaces: The namespace or namespaces to filter by
    """
    if isinstance(namespaces, str):
        def target_namespace_filter(_, __, v: BaseEntity, ___) -> bool:
            return node_has_namespace(v, namespaces)

    elif isinstance(namespaces, Iterable):
        namespaces = set(namespaces)

        def target_namespace_filter(_, __, v: BaseEntity, ___) -> bool:
            return node_has_namespaces(v, namespaces)

    else:
        raise TypeError

    return target_namespace_filter