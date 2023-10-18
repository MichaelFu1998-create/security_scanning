def remove_nodes_by_function_namespace(graph: BELGraph, func: str, namespace: Strings) -> None:
    """Remove nodes with the given function and namespace.

    This might be useful to exclude information learned about distant species, such as excluding all information
    from MGI and RGD in diseases where mice and rats don't give much insight to the human disease mechanism.
    """
    remove_filtered_nodes(graph, function_namespace_inclusion_builder(func, namespace))