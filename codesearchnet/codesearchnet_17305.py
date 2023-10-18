def count_annotation_values(graph: BELGraph, annotation: str) -> Counter:
    """Count in how many edges each annotation appears in a graph

    :param graph: A BEL graph
    :param annotation: The annotation to count
    :return: A Counter from {annotation value: frequency}
    """
    return Counter(iter_annotation_values(graph, annotation))