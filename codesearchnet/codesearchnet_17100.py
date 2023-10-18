def _collapse_variants_by_function(graph: BELGraph, func: str) -> None:
    """Collapse all of the given functions' variants' edges to their parents, in-place."""
    for parent_node, variant_node, data in graph.edges(data=True):
        if data[RELATION] == HAS_VARIANT and parent_node.function == func:
            collapse_pair(graph, from_node=variant_node, to_node=parent_node)