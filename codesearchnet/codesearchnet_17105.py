def collapse_orthologies_by_namespace(graph: BELGraph, victim_namespace: Strings, survivor_namespace: str) -> None:
    """Collapse pairs of nodes with the given namespaces that have orthology relationships.

    :param graph: A BEL Graph
    :param victim_namespace: The namespace(s) of the node to collapse
    :param survivor_namespace: The namespace of the node to keep

    To collapse all MGI nodes to their HGNC orthologs, use:
    >>> collapse_orthologies_by_namespace('MGI', 'HGNC')


    To collapse collapse both MGI and RGD nodes to their HGNC orthologs, use:
    >>> collapse_orthologies_by_namespace(['MGI', 'RGD'], 'HGNC')
    """
    _collapse_edge_by_namespace(graph, victim_namespace, survivor_namespace, ORTHOLOGOUS)