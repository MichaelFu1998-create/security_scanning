def get_neurommsig_scores(graph: BELGraph,
                          genes: List[Gene],
                          annotation: str = 'Subgraph',
                          ora_weight: Optional[float] = None,
                          hub_weight: Optional[float] = None,
                          top_percent: Optional[float] = None,
                          topology_weight: Optional[float] = None,
                          preprocess: bool = False
                          ) -> Optional[Mapping[str, float]]:
    """Preprocess the graph, stratify by the given annotation, then run the NeuroMMSig algorithm on each.

    :param graph: A BEL graph
    :param genes: A list of gene nodes
    :param annotation: The annotation to use to stratify the graph to subgraphs
    :param ora_weight: The relative weight of the over-enrichment analysis score from
     :py:func:`neurommsig_gene_ora`. Defaults to 1.0.
    :param hub_weight: The relative weight of the hub analysis score from :py:func:`neurommsig_hubs`.
     Defaults to 1.0.
    :param top_percent: The percentage of top genes to use as hubs. Defaults to 5% (0.05).
    :param topology_weight: The relative weight of the topolgical analysis core from
     :py:func:`neurommsig_topology`. Defaults to 1.0.
    :param preprocess: If true, preprocess the graph.
    :return: A dictionary from {annotation value: NeuroMMSig composite score}

    Pre-processing steps:

    1. Infer the central dogma with :func:``
    2. Collapse all proteins, RNAs and miRNAs to genes with :func:``
    3. Collapse variants to genes with :func:``
    """
    if preprocess:
        graph = neurommsig_graph_preprocessor.run(graph)

    if not any(gene in graph for gene in genes):
        logger.debug('no genes mapping to graph')
        return

    subgraphs = get_subgraphs_by_annotation(graph, annotation=annotation)

    return get_neurommsig_scores_prestratified(
        subgraphs=subgraphs,
        genes=genes,
        ora_weight=ora_weight,
        hub_weight=hub_weight,
        top_percent=top_percent,
        topology_weight=topology_weight,
    )