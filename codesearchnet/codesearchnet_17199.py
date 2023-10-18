def build_delete_node_by_hash(manager: Manager) -> Callable[[BELGraph, str], None]:
    """Make a delete function that's bound to the manager."""

    @in_place_transformation
    def delete_node_by_hash(graph: BELGraph, node_hash: str) -> None:
        """Remove a node by identifier."""
        node = manager.get_dsl_by_hash(node_hash)
        graph.remove_node(node)

    return delete_node_by_hash