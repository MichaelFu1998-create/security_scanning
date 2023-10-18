def group_nodes_by_annotation_filtered(graph: BELGraph,
                                       node_predicates: NodePredicates = None,
                                       annotation: str = 'Subgraph',
                                       ) -> Mapping[str, Set[BaseEntity]]:
    """Group the nodes occurring in edges by the given annotation, with a node filter applied.

    :param graph: A BEL graph
    :param node_predicates: A predicate or list of predicates (graph, node) -> bool
    :param annotation: The annotation to use for grouping
    :return: A dictionary of {annotation value: set of nodes}
    """
    node_filter = concatenate_node_predicates(node_predicates)

    return {
        key: {
            node
            for node in nodes
            if node_filter(graph, node)
        }
        for key, nodes in group_nodes_by_annotation(graph, annotation).items()
    }