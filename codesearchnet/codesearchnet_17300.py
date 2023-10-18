def get_variants_to_controllers(
        graph: BELGraph,
        node: Protein,
        modifications: Optional[Set[str]] = None,
) -> Mapping[Protein, Set[Protein]]:
    """Get a mapping from variants of the given node to all of its upstream controllers."""
    rv = defaultdict(set)
    variants = variants_of(graph, node, modifications)
    for controller, variant, data in graph.in_edges(variants, data=True):
        if data[RELATION] in CAUSAL_RELATIONS:
            rv[variant].add(controller)
    return rv