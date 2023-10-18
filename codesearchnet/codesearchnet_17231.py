def self_edge_filter(_: BELGraph, source: BaseEntity, target: BaseEntity, __: str) -> bool:
    """Check if the source and target nodes are the same."""
    return source == target