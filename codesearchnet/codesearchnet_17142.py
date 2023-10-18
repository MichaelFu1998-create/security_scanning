def expand_internal_causal(universe: BELGraph, graph: BELGraph) -> None:
    """Add causal edges between entities in the sub-graph.

    Is an extremely thin wrapper around :func:`expand_internal`.

    :param universe: A BEL graph representing the universe of all knowledge
    :param graph: The target BEL graph to enrich with causal relations between contained nodes

    Equivalent to:

    >>> from pybel_tools.mutation import expand_internal
    >>> from pybel.struct.filters.edge_predicates import is_causal_relation
    >>> expand_internal(universe, graph, edge_predicates=is_causal_relation)
    """
    expand_internal(universe, graph, edge_predicates=is_causal_relation)