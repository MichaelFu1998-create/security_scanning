def count_author_publications(graph: BELGraph) -> typing.Counter[str]:
    """Count the number of publications of each author to the given graph."""
    authors = group_as_dict(_iter_author_publiations(graph))
    return Counter(count_dict_values(count_defaultdict(authors)))