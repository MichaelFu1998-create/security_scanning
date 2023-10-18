def get_evidences_by_pmid(graph: BELGraph, pmids: Union[str, Iterable[str]]):
    """Get a dictionary from the given PubMed identifiers to the sets of all evidence strings associated with each
    in the graph.

    :param graph: A BEL graph
    :param pmids: An iterable of PubMed identifiers, as strings. Is consumed and converted to a set.
    :return: A dictionary of {pmid: set of all evidence strings}
    :rtype: dict
    """
    result = defaultdict(set)

    for _, _, _, data in filter_edges(graph, build_pmid_inclusion_filter(pmids)):
        result[data[CITATION][CITATION_REFERENCE]].add(data[EVIDENCE])

    return dict(result)