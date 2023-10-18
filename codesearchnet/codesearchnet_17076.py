def get_authors_by_keyword(keyword: str, graph=None, authors=None) -> Set[str]:
    """Get authors for whom the search term is a substring.
    
    :param pybel.BELGraph graph: A BEL graph
    :param keyword: The keyword to search the author strings for
    :param set[str] authors: An optional set of pre-cached authors calculated from the graph
    :return: A set of authors with the keyword as a substring
    """
    keyword_lower = keyword.lower()

    if authors is not None:
        return {
            author
            for author in authors
            if keyword_lower in author.lower()
        }

    if graph is None:
        raise ValueError('Graph not supplied')

    return {
        author
        for author in get_authors(graph)
        if keyword_lower in author.lower()
    }