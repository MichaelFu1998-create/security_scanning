def get_subgraph_peripheral_nodes(graph: BELGraph,
                                  subgraph: Iterable[BaseEntity],
                                  node_predicates: NodePredicates = None,
                                  edge_predicates: EdgePredicates = None,
                                  ):
    """Get a summary dictionary of all peripheral nodes to a given sub-graph.

    :return: A dictionary of {external node: {'successor': {internal node: list of (key, dict)},
                                            'predecessor': {internal node: list of (key, dict)}}}
    :rtype: dict

    For example, it might be useful to quantify the number of predecessors and successors:

    >>> from pybel.struct.filters import exclude_pathology_filter
    >>> value = 'Blood vessel dilation subgraph'
    >>> sg = get_subgraph_by_annotation_value(graph, annotation='Subgraph', value=value)
    >>> p = get_subgraph_peripheral_nodes(graph, sg, node_predicates=exclude_pathology_filter)
    >>> for node in sorted(p, key=lambda n: len(set(p[n]['successor']) | set(p[n]['predecessor'])), reverse=True):
    >>>     if 1 == len(p[value][node]['successor']) or 1 == len(p[value][node]['predecessor']):
    >>>         continue
    >>>     print(node,
    >>>           len(p[node]['successor']),
    >>>           len(p[node]['predecessor']),
    >>>           len(set(p[node]['successor']) | set(p[node]['predecessor'])))
    """
    node_filter = concatenate_node_predicates(node_predicates=node_predicates)
    edge_filter = and_edge_predicates(edge_predicates=edge_predicates)

    result = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for u, v, k, d in get_peripheral_successor_edges(graph, subgraph):
        if not node_filter(graph, v) or not node_filter(graph, u) or not edge_filter(graph, u, v, k):
            continue
        result[v]['predecessor'][u].append((k, d))

    for u, v, k, d in get_peripheral_predecessor_edges(graph, subgraph):
        if not node_filter(graph, v) or not node_filter(graph, u) or not edge_filter(graph, u, v, k):
            continue
        result[u]['successor'][v].append((k, d))

    return result