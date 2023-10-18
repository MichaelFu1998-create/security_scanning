def node_inclusion_filter_builder(nodes: Iterable[BaseEntity]) -> NodePredicate:
    """Build a filter that only passes on nodes in the given list.

    :param nodes: An iterable of BEL nodes
    """
    node_set = set(nodes)

    def inclusion_filter(_: BELGraph, node: BaseEntity) -> bool:
        """Pass only for a node that is in the enclosed node list.

        :return: If the node is contained within the enclosed node list
        """
        return node in node_set

    return inclusion_filter