def rewire_variants_to_genes(graph: BELGraph) -> None:
    """Find all protein variants that are pointing to a gene and not a protein and fixes them by changing their
    function to be :data:`pybel.constants.GENE`, in place

    A use case is after running :func:`collapse_to_genes`.
    """
    mapping = {}

    for node in graph:
        if not isinstance(node, Protein) or not node.variants:
            continue

        mapping[node] = Gene(
            name=node.name,
            namespace=node.namespace,
            identifier=node.identifier,
            variants=node.variants,
        )

    nx.relabel_nodes(graph, mapping, copy=False)