def count_citations(graph: BELGraph, **annotations) -> Counter:
    """Counts the citations in a graph based on a given filter

    :param graph: A BEL graph
    :param dict annotations: The annotation filters to use
    :return: A counter from {(citation type, citation reference): frequency}
    """
    citations = defaultdict(set)

    annotation_dict_filter = build_edge_data_filter(annotations)

    for u, v, _, d in filter_edges(graph, annotation_dict_filter):
        if CITATION not in d:
            continue

        citations[u, v].add((d[CITATION][CITATION_TYPE], d[CITATION][CITATION_REFERENCE].strip()))

    return Counter(itt.chain.from_iterable(citations.values()))