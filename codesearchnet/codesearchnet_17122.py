def get_neurommsig_score(graph: BELGraph,
                         genes: List[Gene],
                         ora_weight: Optional[float] = None,
                         hub_weight: Optional[float] = None,
                         top_percent: Optional[float] = None,
                         topology_weight: Optional[float] = None) -> float:
    """Calculate the composite NeuroMMSig Score for a given list of genes.

    :param graph: A BEL graph
    :param genes: A list of gene nodes
    :param ora_weight: The relative weight of the over-enrichment analysis score from
     :py:func:`neurommsig_gene_ora`. Defaults to 1.0.
    :param hub_weight: The relative weight of the hub analysis score from :py:func:`neurommsig_hubs`.
     Defaults to 1.0.
    :param top_percent: The percentage of top genes to use as hubs. Defaults to 5% (0.05).
    :param topology_weight: The relative weight of the topolgical analysis core from
     :py:func:`neurommsig_topology`. Defaults to 1.0.
    :return: The NeuroMMSig composite score
    """
    ora_weight = ora_weight or 1.0
    hub_weight = hub_weight or 1.0
    topology_weight = topology_weight or 1.0
    total_weight = ora_weight + hub_weight + topology_weight

    genes = list(genes)

    ora_score = neurommsig_gene_ora(graph, genes)
    hub_score = neurommsig_hubs(graph, genes, top_percent=top_percent)
    topology_score = neurommsig_topology(graph, genes)

    weighted_sum = (
            ora_weight * ora_score +
            hub_weight * hub_score +
            topology_weight * topology_score
    )

    return weighted_sum / total_weight