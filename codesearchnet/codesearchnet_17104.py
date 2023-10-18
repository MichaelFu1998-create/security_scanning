def collapse_equivalencies_by_namespace(graph: BELGraph, victim_namespace: Strings, survivor_namespace: str) -> None:
    """Collapse pairs of nodes with the given namespaces that have equivalence relationships.
    
    :param graph: A BEL graph
    :param victim_namespace: The namespace(s) of the node to collapse
    :param survivor_namespace: The namespace of the node to keep

    To convert all ChEBI names to InChI keys, assuming there are appropriate equivalence relations between nodes with
    those namespaces:
    
    >>> collapse_equivalencies_by_namespace(graph, 'CHEBI', 'CHEBIID')
    >>> collapse_equivalencies_by_namespace(graph, 'CHEBIID', 'INCHI')
    """
    _collapse_edge_by_namespace(graph, victim_namespace, survivor_namespace, EQUIVALENT_TO)