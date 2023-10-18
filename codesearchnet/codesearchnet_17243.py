def build_pmid_exclusion_filter(pmids: Strings) -> EdgePredicate:
    """Fail for edges with citations whose references are one of the given PubMed identifiers.

    :param pmids: A PubMed identifier or list of PubMed identifiers to filter against
    """
    if isinstance(pmids, str):
        @edge_predicate
        def pmid_exclusion_filter(data: EdgeData) -> bool:
            """Fail for edges with PubMed citations matching the contained PubMed identifier.

            :return: If the edge has a PubMed citation with the contained PubMed identifier
            """
            return has_pubmed(data) and data[CITATION][CITATION_REFERENCE] != pmids

    elif isinstance(pmids, Iterable):
        pmids = set(pmids)

        @edge_predicate
        def pmid_exclusion_filter(data: EdgeData) -> bool:
            """Pass for edges with PubMed citations matching one of the contained PubMed identifiers.

            :return: If the edge has a PubMed citation with one of the contained PubMed identifiers
            """
            return has_pubmed(data) and data[CITATION][CITATION_REFERENCE] not in pmids

    else:
        raise TypeError

    return pmid_exclusion_filter