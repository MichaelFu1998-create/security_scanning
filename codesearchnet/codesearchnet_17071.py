def _generate_citation_dict(graph: BELGraph) -> Mapping[str, Mapping[Tuple[BaseEntity, BaseEntity], str]]:
    """Prepare a citation data dictionary from a graph.

    :return: A dictionary of dictionaries {citation type: {(source, target): citation reference}
    """
    results = defaultdict(lambda: defaultdict(set))

    for u, v, data in graph.edges(data=True):
        if CITATION not in data:
            continue
        results[data[CITATION][CITATION_TYPE]][u, v].add(data[CITATION][CITATION_REFERENCE].strip())

    return dict(results)