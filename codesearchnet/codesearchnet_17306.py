def count_annotation_values_filtered(graph: BELGraph,
                                     annotation: str,
                                     source_predicate: Optional[NodePredicate] = None,
                                     target_predicate: Optional[NodePredicate] = None,
                                     ) -> Counter:
    """Count in how many edges each annotation appears in a graph, but filter out source nodes and target nodes.

    See :func:`pybel_tools.utils.keep_node` for a basic filter.

    :param graph: A BEL graph
    :param annotation: The annotation to count
    :param source_predicate: A predicate (graph, node) -> bool for keeping source nodes
    :param target_predicate: A predicate (graph, node) -> bool for keeping target nodes
    :return: A Counter from {annotation value: frequency}
    """
    if source_predicate and target_predicate:
        return Counter(
            data[ANNOTATIONS][annotation]
            for u, v, data in graph.edges(data=True)
            if edge_has_annotation(data, annotation) and source_predicate(graph, u) and target_predicate(graph, v)
        )
    elif source_predicate:
        return Counter(
            data[ANNOTATIONS][annotation]
            for u, v, data in graph.edges(data=True)
            if edge_has_annotation(data, annotation) and source_predicate(graph, u)
        )
    elif target_predicate:
        return Counter(
            data[ANNOTATIONS][annotation]
            for u, v, data in graph.edges(data=True)
            if edge_has_annotation(data, annotation) and target_predicate(graph, u)
        )
    else:
        return Counter(
            data[ANNOTATIONS][annotation]
            for u, v, data in graph.edges(data=True)
            if edge_has_annotation(data, annotation)
        )