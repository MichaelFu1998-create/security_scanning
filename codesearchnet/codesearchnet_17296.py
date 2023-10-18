def function_exclusion_filter_builder(func: Strings) -> NodePredicate:
    """Build a filter that fails on nodes of the given function(s).

    :param func: A BEL Function or list/set/tuple of BEL functions
    """
    if isinstance(func, str):
        def function_exclusion_filter(_: BELGraph, node: BaseEntity) -> bool:
            """Pass only for a node that doesn't have the enclosed function.

            :return: If the node doesn't have the enclosed function
            """
            return node[FUNCTION] != func

        return function_exclusion_filter

    elif isinstance(func, Iterable):
        functions = set(func)

        def functions_exclusion_filter(_: BELGraph, node: BaseEntity) -> bool:
            """Pass only for a node that doesn't have the enclosed functions.

            :return: If the node doesn't have the enclosed functions
            """
            return node[FUNCTION] not in functions

        return functions_exclusion_filter

    raise ValueError('Invalid type for argument: {}'.format(func))