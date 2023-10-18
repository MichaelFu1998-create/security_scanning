def function_namespace_inclusion_builder(func: str, namespace: Strings) -> NodePredicate:
    """Build a filter function for matching the given BEL function with the given namespace or namespaces.

    :param func: A BEL function
    :param namespace: The namespace to search by
    """
    if isinstance(namespace, str):
        def function_namespaces_filter(_: BELGraph, node: BaseEntity) -> bool:
            """Pass only for nodes that have the enclosed function and enclosed namespace."""
            if func != node[FUNCTION]:
                return False
            return NAMESPACE in node and node[NAMESPACE] == namespace

    elif isinstance(namespace, Iterable):
        namespaces = set(namespace)

        def function_namespaces_filter(_: BELGraph, node: BaseEntity) -> bool:
            """Pass only for nodes that have the enclosed function and namespace in the enclose set."""
            if func != node[FUNCTION]:
                return False
            return NAMESPACE in node and node[NAMESPACE] in namespaces

    else:
        raise ValueError('Invalid type for argument: {}'.format(namespace))

    return function_namespaces_filter