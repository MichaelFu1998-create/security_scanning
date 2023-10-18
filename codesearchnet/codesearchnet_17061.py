def get_jens_unstable(graph: BELGraph) -> Iterable[NodeTriple]:
    """Yield triples of nodes (A, B, C) where ``A -> B``, ``A -| C``, and ``C positiveCorrelation A``.

    Calculated efficiently using the Jens Transformation.
    """
    r = jens_transformation_alpha(graph)
    return get_triangles(r)