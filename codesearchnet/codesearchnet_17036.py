def count_subgraph_sizes(graph: BELGraph, annotation: str = 'Subgraph') -> Counter[int]:
    """Count the number of nodes in each subgraph induced by an annotation.

    :param annotation: The annotation to group by and compare. Defaults to 'Subgraph'
    :return: A dictionary from {annotation value: number of nodes}
    """
    return count_dict_values(group_nodes_by_annotation(graph, annotation))