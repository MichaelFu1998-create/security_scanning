def has_protein_modification_increases_activity(graph: BELGraph,
                                                source: BaseEntity,
                                                target: BaseEntity,
                                                key: str,
                                                ) -> bool:
    """Check if pmod of source causes activity of target."""
    edge_data = graph[source][target][key]
    return has_protein_modification(graph, source) and part_has_modifier(edge_data, OBJECT, ACTIVITY)