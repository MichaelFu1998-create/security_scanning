def neurommsig_hubs(graph: BELGraph, genes: List[Gene], top_percent: Optional[float] = None) -> float:
    """Calculate the percentage of target genes mappable to the graph.
    
    Assume: graph central dogma inferred, collapsed to genes, collapsed variants, graph has more than 20 nodes
    
    :param graph: A BEL graph
    :param genes: A list of nodes
    :param top_percent: The percentage of top genes to use as hubs. Defaults to 5% (0.05).
    """
    top_percent = top_percent or 0.05

    if graph.number_of_nodes() < 20:
        logger.debug('Graph has less than 20 nodes')
        return 0.0

    graph_genes = set(get_nodes_by_function(graph, GENE))

    bc = Counter({
        node: betweenness_centrality
        for node, betweenness_centrality in calculate_betweenness_centality(graph).items()
        if node in graph_genes
    })

    # TODO consider continuous analog with weighting by percentile
    number_central_nodes = int(len(graph_genes) * top_percent)

    if number_central_nodes < 1:
        number_central_nodes = 1

    number_mappable_central_nodes = sum(
        node in genes
        for node in bc.most_common(number_central_nodes)
    )

    return number_mappable_central_nodes / number_central_nodes