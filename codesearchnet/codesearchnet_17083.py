def enrich_pubmed_citations(graph: BELGraph, manager: Manager) -> Set[str]:
    """Overwrite all PubMed citations with values from NCBI's eUtils lookup service.

    :return: A set of PMIDs for which the eUtils service crashed
    """
    pmids = get_pubmed_identifiers(graph)
    pmid_data, errors = get_citations_by_pmids(manager=manager, pmids=pmids)

    for u, v, k in filter_edges(graph, has_pubmed):
        pmid = graph[u][v][k][CITATION][CITATION_REFERENCE].strip()

        if pmid not in pmid_data:
            log.warning('Missing data for PubMed identifier: %s', pmid)
            errors.add(pmid)
            continue

        graph[u][v][k][CITATION].update(pmid_data[pmid])

    return errors