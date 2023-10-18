def count_top_centrality(graph: BELGraph, number: Optional[int] = 30) -> Mapping[BaseEntity, int]:
    """Get top centrality dictionary."""
    dd = nx.betweenness_centrality(graph)
    dc = Counter(dd)
    return dict(dc.most_common(number))