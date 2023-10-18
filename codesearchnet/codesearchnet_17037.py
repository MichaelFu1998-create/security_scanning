def calculate_subgraph_edge_overlap(
        graph: BELGraph,
        annotation: str = 'Subgraph'
) -> Tuple[
    Mapping[str, EdgeSet],
    Mapping[str, Mapping[str, EdgeSet]],
    Mapping[str, Mapping[str, EdgeSet]],
    Mapping[str, Mapping[str, float]],
]:
    """Build a DatafFame to show the overlap between different sub-graphs.

    Options:
    1. Total number of edges overlap (intersection)
    2. Percentage overlap (tanimoto similarity)

    :param graph: A BEL graph
    :param annotation: The annotation to group by and compare. Defaults to 'Subgraph'
    :return: {subgraph: set of edges}, {(subgraph 1, subgraph2): set of intersecting edges},
            {(subgraph 1, subgraph2): set of unioned edges}, {(subgraph 1, subgraph2): tanimoto similarity},
    """
    sg2edge = defaultdict(set)

    for u, v, d in graph.edges(data=True):
        if not edge_has_annotation(d, annotation):
            continue
        sg2edge[d[ANNOTATIONS][annotation]].add((u, v))

    subgraph_intersection = defaultdict(dict)
    subgraph_union = defaultdict(dict)
    result = defaultdict(dict)

    for sg1, sg2 in itt.product(sg2edge, repeat=2):
        subgraph_intersection[sg1][sg2] = sg2edge[sg1] & sg2edge[sg2]
        subgraph_union[sg1][sg2] = sg2edge[sg1] | sg2edge[sg2]
        result[sg1][sg2] = len(subgraph_intersection[sg1][sg2]) / len(subgraph_union[sg1][sg2])

    return sg2edge, subgraph_intersection, subgraph_union, result