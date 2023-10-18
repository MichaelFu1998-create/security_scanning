def node_exclusion_filter_builder(nodes: Iterable[BaseEntity]) -> NodePredicate:
    """Build a filter that fails on nodes in the given list."""
    node_set = set(nodes)

    def exclusion_filter(_: BELGraph, node: BaseEntity) -> bool:
        """Pass only for a node that isn't in the enclosed node list

        :return: If the node isn't contained within the enclosed node list
        """
        return node not in node_set

    return exclusion_filter