def neurommsig_gene_ora(graph: BELGraph, genes: List[Gene]) -> float:
    """Calculate the percentage of target genes mappable to the graph.
    
    Assume: graph central dogma inferred, collapsed to genes, collapsed variants 
    """
    graph_genes = set(get_nodes_by_function(graph, GENE))
    return len(graph_genes.intersection(genes)) / len(graph_genes)