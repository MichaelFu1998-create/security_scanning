def get_most_common_errors(graph: BELGraph, n: Optional[int] = 20):
    """Get the (n) most common errors in a graph."""
    return count_dict_values(group_errors(graph)).most_common(n)