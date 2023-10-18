def count_authors_by_annotation(graph: BELGraph, annotation: str = 'Subgraph') -> Mapping[str, typing.Counter[str]]:
    """Group the author counters by sub-graphs induced by the annotation.

    :param graph: A BEL graph
    :param annotation: The annotation to use to group the graph
    :return: A dictionary of Counters {subgraph name: Counter from {author: frequency}}
    """
    authors = group_as_dict(_iter_authors_by_annotation(graph, annotation=annotation))
    return count_defaultdict(authors)