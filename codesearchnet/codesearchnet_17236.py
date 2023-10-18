def complex_increases_activity(graph: BELGraph, u: BaseEntity, v: BaseEntity, key: str) -> bool:
    """Return if the formation of a complex with u increases the activity of v."""
    return (
        isinstance(u, (ComplexAbundance, NamedComplexAbundance)) and
        complex_has_member(graph, u, v) and
        part_has_modifier(graph[u][v][key], OBJECT, ACTIVITY)
    )