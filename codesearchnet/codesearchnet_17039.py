def summarize_subgraph_node_overlap(graph: BELGraph, node_predicates=None, annotation: str = 'Subgraph'):
    """Calculate the subgraph similarity tanimoto similarity in nodes passing the given filter.

    Provides an alternate view on subgraph similarity, from a more node-centric view
    """
    r1 = group_nodes_by_annotation_filtered(graph, node_predicates=node_predicates, annotation=annotation)
    return calculate_tanimoto_set_distances(r1)