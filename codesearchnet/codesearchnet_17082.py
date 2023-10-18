def count_confidences(graph: BELGraph) -> typing.Counter[str]:
    """Count the confidences in the graph."""
    return Counter(
        (
            'None'
            if ANNOTATIONS not in data or 'Confidence' not in data[ANNOTATIONS] else
            list(data[ANNOTATIONS]['Confidence'])[0]
        )
        for _, _, data in graph.edges(data=True)
        if CITATION in data  # don't bother with unqualified statements
    )