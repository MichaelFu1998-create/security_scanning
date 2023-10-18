def node_has_namespaces(node: BaseEntity, namespaces: Set[str]) -> bool:
    """Pass for nodes that have one of the given namespaces."""
    ns = node.get(NAMESPACE)
    return ns is not None and ns in namespaces