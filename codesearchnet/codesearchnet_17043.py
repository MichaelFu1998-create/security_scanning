def prerender(graph: BELGraph) -> Mapping[str, Mapping[str, Any]]:
    """Generate the annotations JSON for Ideogram."""
    import bio2bel_hgnc
    from bio2bel_hgnc.models import HumanGene

    graph: BELGraph = graph.copy()
    enrich_protein_and_rna_origins(graph)
    collapse_all_variants(graph)
    genes: Set[Gene] = get_nodes_by_function(graph, GENE)
    hgnc_symbols = {
        gene.name
        for gene in genes
        if gene.namespace.lower() == 'hgnc'
    }

    result = {}

    hgnc_manager = bio2bel_hgnc.Manager()
    human_genes = (
        hgnc_manager.session
            .query(HumanGene.symbol, HumanGene.location)
            .filter(HumanGene.symbol.in_(hgnc_symbols))
            .all()
    )
    for human_gene in human_genes:
        result[human_gene.symbol] = {
            'name': human_gene.symbol,
            'chr': (
                human_gene.location.split('q')[0]
                if 'q' in human_gene.location else
                human_gene.location.split('p')[0]
            ),
        }

    df = get_df()

    for _, (gene_id, symbol, start, stop) in df[df['Symbol'].isin(hgnc_symbols)].iterrows():
        result[symbol]['start'] = start
        result[symbol]['stop'] = stop

    return result