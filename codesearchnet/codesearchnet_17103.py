def _collapse_edge_by_namespace(graph: BELGraph,
                                victim_namespaces: Strings,
                                survivor_namespaces: str,
                                relations: Strings) -> None:
    """Collapse pairs of nodes with the given namespaces that have the given relationship.

    :param graph: A BEL Graph
    :param victim_namespaces: The namespace(s) of the node to collapse
    :param survivor_namespaces: The namespace of the node to keep
    :param relations: The relation(s) to search
    """
    relation_filter = build_relation_predicate(relations)
    source_namespace_filter = build_source_namespace_filter(victim_namespaces)
    target_namespace_filter = build_target_namespace_filter(survivor_namespaces)

    edge_predicates = [
        relation_filter,
        source_namespace_filter,
        target_namespace_filter
    ]

    _collapse_edge_passing_predicates(graph, edge_predicates=edge_predicates)