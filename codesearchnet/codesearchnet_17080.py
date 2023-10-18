def get_citation_years(graph: BELGraph) -> List[Tuple[int, int]]:
    """Create a citation timeline counter from the graph."""
    return create_timeline(count_citation_years(graph))