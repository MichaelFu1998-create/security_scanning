def data_contains_key_builder(key: str) -> NodePredicate:  # noqa: D202
    """Build a filter that passes only on nodes that have the given key in their data dictionary.

    :param key: A key for the node's data dictionary
    """

    def data_contains_key(_: BELGraph, node: BaseEntity) -> bool:
        """Pass only for a node that contains the enclosed key in its data dictionary.

        :return: If the node contains the enclosed key in its data dictionary
        """
        return key in node

    return data_contains_key