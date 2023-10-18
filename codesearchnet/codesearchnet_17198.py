def build_expand_node_neighborhood_by_hash(manager: Manager) -> Callable[[BELGraph, BELGraph, str], None]:
    """Make an expand function that's bound to the manager."""

    @uni_in_place_transformation
    def expand_node_neighborhood_by_hash(universe: BELGraph, graph: BELGraph, node_hash: str) -> None:
        """Expand around the neighborhoods of a node by identifier."""
        node = manager.get_dsl_by_hash(node_hash)
        return expand_node_neighborhood(universe, graph, node)

    return expand_node_neighborhood_by_hash