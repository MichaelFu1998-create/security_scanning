def enrich_variants(graph: BELGraph, func: Union[None, str, Iterable[str]] = None):
    """Add the reference nodes for all variants of the given function.

    :param graph: The target BEL graph to enrich
    :param func: The function by which the subject of each triple is filtered. Defaults to the set of protein, rna,
     mirna, and gene.
    """
    if func is None:
        func = {PROTEIN, RNA, MIRNA, GENE}

    nodes = list(get_nodes_by_function(graph, func))
    for u in nodes:
        parent = u.get_parent()

        if parent is None:
            continue

        if parent not in graph:
            graph.add_has_variant(parent, u)