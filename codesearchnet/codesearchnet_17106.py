def collapse_entrez_equivalencies(graph: BELGraph):
    """Collapse all equivalence edges away from Entrez. Assumes well formed, 2-way equivalencies."""
    relation_filter = build_relation_predicate(EQUIVALENT_TO)
    source_namespace_filter = build_source_namespace_filter(['EGID', 'EG', 'ENTREZ'])

    edge_predicates = [
        relation_filter,
        source_namespace_filter,
    ]

    _collapse_edge_passing_predicates(graph, edge_predicates=edge_predicates)