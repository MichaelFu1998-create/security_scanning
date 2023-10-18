def search_node_namespace_names(graph, query, namespace):
    """Search for nodes with the given namespace(s) and whose names containing a given string(s).

    :param pybel.BELGraph graph: A BEL graph
    :param query: The search query
    :type query: str or iter[str]
    :param namespace: The namespace(s) to filter
    :type namespace: str or iter[str]
    :return: An iterator over nodes whose names match the search query
    :rtype: iter
    """
    node_predicates = [
        namespace_inclusion_builder(namespace),
        build_node_name_search(query)
    ]

    return filter_nodes(graph, node_predicates)