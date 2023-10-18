def jens_transformation_alpha(graph: BELGraph) -> DiGraph:
    """Apply Jens' transformation (Type 1) to the graph.

    1. Induce a sub-graph over causal + correlative edges
    2. Transform edges by the following rules:
        - increases => increases
        - decreases => backwards increases
        - positive correlation => two way increases
        - negative correlation => delete

    The resulting graph can be used to search for 3-cycles, which now symbolize unstable triplets where ``A -> B``,
    ``A -| C`` and ``B positiveCorrelation C``.
    """
    result = DiGraph()

    for u, v, d in graph.edges(data=True):
        relation = d[RELATION]

        if relation == POSITIVE_CORRELATION:
            result.add_edge(u, v)
            result.add_edge(v, u)

        elif relation in CAUSAL_INCREASE_RELATIONS:
            result.add_edge(u, v)

        elif relation in CAUSAL_DECREASE_RELATIONS:
            result.add_edge(v, u)

    return result