def enrich_unqualified(graph: BELGraph):
    """Enrich the sub-graph with the unqualified edges from the graph.

    The reason you might want to do this is you induce a sub-graph from the original graph based on an annotation
    filter, but the unqualified edges that don't have annotations that most likely connect elements within your graph
    are not included.

    .. seealso::

        This function thinly wraps the successive application of the following functions:

        - :func:`enrich_complexes`
        - :func:`enrich_composites`
        - :func:`enrich_reactions`
        - :func:`enrich_variants`

    Equivalent to:

    >>> enrich_complexes(graph)
    >>> enrich_composites(graph)
    >>> enrich_reactions(graph)
    >>> enrich_variants(graph)
    """
    enrich_complexes(graph)
    enrich_composites(graph)
    enrich_reactions(graph)
    enrich_variants(graph)