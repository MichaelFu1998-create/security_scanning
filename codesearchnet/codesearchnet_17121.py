def get_neurommsig_scores_prestratified(subgraphs: Mapping[str, BELGraph],
                                        genes: List[Gene],
                                        ora_weight: Optional[float] = None,
                                        hub_weight: Optional[float] = None,
                                        top_percent: Optional[float] = None,
                                        topology_weight: Optional[float] = None,
                                        ) -> Optional[Mapping[str, float]]:
    """Takes a graph stratification and runs neurommsig on each

    :param subgraphs: A pre-stratified set of graphs
    :param genes: A list of gene nodes
    :param ora_weight: The relative weight of the over-enrichment analysis score from
     :py:func:`neurommsig_gene_ora`. Defaults to 1.0.
    :param hub_weight: The relative weight of the hub analysis score from :py:func:`neurommsig_hubs`.
     Defaults to 1.0.
    :param top_percent: The percentage of top genes to use as hubs. Defaults to 5% (0.05).
    :param topology_weight: The relative weight of the topolgical analysis core from
     :py:func:`neurommsig_topology`. Defaults to 1.0.
    :return: A dictionary from {annotation value: NeuroMMSig composite score}

    Pre-processing steps:

    1. Infer the central dogma with :func:``
    2. Collapse all proteins, RNAs and miRNAs to genes with :func:``
    3. Collapse variants to genes with :func:``
    """
    return {
        name: get_neurommsig_score(
            graph=subgraph,
            genes=genes,
            ora_weight=ora_weight,
            hub_weight=hub_weight,
            top_percent=top_percent,
            topology_weight=topology_weight,
        )
        for name, subgraph in subgraphs.items()
    }