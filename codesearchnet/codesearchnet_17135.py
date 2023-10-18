def expand_periphery(universe: BELGraph,
                     graph: BELGraph,
                     node_predicates: NodePredicates = None,
                     edge_predicates: EdgePredicates = None,
                     threshold: int = 2,
                     ) -> None:
    """Iterates over all possible edges, peripheral to a given subgraph, that could be added from the given graph.
    Edges could be added if they go to nodes that are involved in relationships that occur with more than the
    threshold (default 2) number of nodes in the subgraph.

    :param universe: The universe of BEL knowledge
    :param graph: The (sub)graph to expand
    :param threshold: Minimum frequency of betweenness occurrence to add a gap node

    A reasonable edge filter to use is :func:`pybel_tools.filters.keep_causal_edges` because this function can allow
    for huge expansions if there happen to be hub nodes.
    """
    nd = get_subgraph_peripheral_nodes(universe, graph, node_predicates=node_predicates,
                                       edge_predicates=edge_predicates)

    for node, dd in nd.items():
        pred_d = dd['predecessor']
        succ_d = dd['successor']

        in_subgraph_connections = set(pred_d) | set(succ_d)

        if threshold > len(in_subgraph_connections):
            continue

        graph.add_node(node, attr_dict=universe[node])

        for u, edges in pred_d.items():
            for k, d in edges:
                safe_add_edge(graph, u, node, k, d)

        for v, edges in succ_d.items():
            for k, d in edges:
                safe_add_edge(graph, node, v, k, d)