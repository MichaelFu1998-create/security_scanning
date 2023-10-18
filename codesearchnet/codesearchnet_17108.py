def collapse_to_protein_interactions(graph: BELGraph) -> BELGraph:
    """Collapse to a graph made of only causal gene/protein edges."""
    rv: BELGraph = graph.copy()

    collapse_to_genes(rv)

    def is_edge_ppi(_: BELGraph, u: BaseEntity, v: BaseEntity, __: str) -> bool:
        """Check if an edge is a PPI."""
        return isinstance(u, Gene) and isinstance(v, Gene)

    return get_subgraph_by_edge_filter(rv, edge_predicates=[has_polarity, is_edge_ppi])