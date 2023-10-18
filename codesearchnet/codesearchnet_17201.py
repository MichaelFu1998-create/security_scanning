def get_matrix_index(graph: BELGraph) -> Set[str]:
    """Return set of HGNC names from Proteins/Rnas/Genes/miRNA, nodes that can be used by SPIA."""
    # TODO: Using HGNC Symbols for now
    return {
        node.name
        for node in graph
        if isinstance(node, CentralDogma) and node.namespace.upper() == 'HGNC'
    }