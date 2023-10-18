def count_citations_by_annotation(graph: BELGraph, annotation: str) -> Mapping[str, typing.Counter[str]]:
    """Group the citation counters by subgraphs induced by the annotation.

    :param graph: A BEL graph
    :param annotation: The annotation to use to group the graph
    :return: A dictionary of Counters {subgraph name: Counter from {citation: frequency}}
    """
    citations = defaultdict(lambda: defaultdict(set))
    for u, v, data in graph.edges(data=True):
        if not edge_has_annotation(data, annotation) or CITATION not in data:
            continue

        k = data[ANNOTATIONS][annotation]

        citations[k][u, v].add((data[CITATION][CITATION_TYPE], data[CITATION][CITATION_REFERENCE].strip()))

    return {k: Counter(itt.chain.from_iterable(v.values())) for k, v in citations.items()}