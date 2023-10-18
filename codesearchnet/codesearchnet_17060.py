def jens_transformation_beta(graph: BELGraph) -> DiGraph:
    """Apply Jens' Transformation (Type 2) to the graph.

    1. Induce a sub-graph over causal and correlative relations
    2. Transform edges with the following rules:
        - increases => backwards decreases
        - decreases => decreases
        - positive correlation => delete
        - negative correlation => two way decreases

    The resulting graph can be used to search for 3-cycles, which now symbolize stable triples where ``A -> B``,
    ``A -| C`` and ``B negativeCorrelation C``.
    """
    result = DiGraph()

    for u, v, d in graph.edges(data=True):
        relation = d[RELATION]

        if relation == NEGATIVE_CORRELATION:
            result.add_edge(u, v)
            result.add_edge(v, u)

        elif relation in CAUSAL_INCREASE_RELATIONS:
            result.add_edge(v, u)

        elif relation in CAUSAL_DECREASE_RELATIONS:
            result.add_edge(u, v)

    return result