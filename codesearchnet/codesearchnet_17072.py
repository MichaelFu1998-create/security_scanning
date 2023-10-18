def get_pmid_by_keyword(keyword: str,
                        graph: Optional[BELGraph] = None,
                        pubmed_identifiers: Optional[Set[str]] = None,
                        ) -> Set[str]:
    """Get the set of PubMed identifiers beginning with the given keyword string.
    
    :param keyword: The beginning of a PubMed identifier
    :param graph: A BEL graph
    :param pubmed_identifiers: A set of pre-cached PubMed identifiers
    :return: A set of PubMed identifiers starting with the given string
    """
    if pubmed_identifiers is not None:
        return {
            pubmed_identifier
            for pubmed_identifier in pubmed_identifiers
            if pubmed_identifier.startswith(keyword)
        }

    if graph is None:
        raise ValueError('Graph not supplied')

    return {
        pubmed_identifier
        for pubmed_identifier in iterate_pubmed_identifiers(graph)
        if pubmed_identifier.startswith(keyword)
    }