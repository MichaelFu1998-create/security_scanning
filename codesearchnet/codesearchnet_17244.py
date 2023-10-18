def node_has_namespace(node: BaseEntity, namespace: str) -> bool:
    """Pass for nodes that have the given namespace."""
    ns = node.get(NAMESPACE)
    return ns is not None and ns == namespace