def summarize_subgraph_edge_overlap(graph: BELGraph, annotation: str = 'Subgraph') -> Mapping[str, Mapping[str, float]]:
    """Return a similarity matrix between all subgraphs (or other given annotation).

    :param annotation: The annotation to group by and compare. Defaults to :code:`"Subgraph"`
    :return: A similarity matrix in a dict of dicts
    :rtype: dict
    """
    _, _, _, subgraph_overlap = calculate_subgraph_edge_overlap(graph, annotation)
    return subgraph_overlap