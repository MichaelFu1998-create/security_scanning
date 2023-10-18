def get_mapped_nodes(graph: BELGraph, namespace: str, names: Iterable[str]) -> Mapping[BaseEntity, Set[BaseEntity]]:
    """Return a dict with keys: nodes that match the namespace and in names and values other nodes (complexes, variants, orthologous...) or this node.
    
    :param graph: A BEL graph
    :param namespace: The namespace to search
    :param names: List or set of values from which we want to map nodes from
    :return: Main node to variants/groups.
    """
    parent_to_variants = defaultdict(set)
    names = set(names)

    for u, v, d in graph.edges(data=True):
        if d[RELATION] in {HAS_MEMBER, HAS_COMPONENT} and v.get(NAMESPACE) == namespace and v.get(NAME) in names:
            parent_to_variants[v].add(u)

        elif d[RELATION] == HAS_VARIANT and u.get(NAMESPACE) == namespace and u.get(NAME) in names:
            parent_to_variants[u].add(v)

        elif d[RELATION] == ORTHOLOGOUS and u.get(NAMESPACE) == namespace and u.get(NAME) in names:
            parent_to_variants[u].add(v)

    return dict(parent_to_variants)