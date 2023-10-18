def percolation_graph(graph, spanning_cluster=True):
    """
    Prepare the (internal) percolation graph from a given graph

    Helper function to prepare the given graph for spanning cluster detection
    (if required).
    Basically it strips off the auxiliary nodes and edges again.
    It also returns fundamental graph quantitities (number of nodes and edges).

    Parameters
    ----------
    graph
    spanning_cluster

    Returns
    -------
    ret : tuple

    """
    ret = dict()

    ret['graph'] = graph
    ret['spanning_cluster'] = bool(spanning_cluster)

    # initialize percolation graph
    if spanning_cluster:
        spanning_auxiliary_node_attributes = nx.get_node_attributes(
            graph, 'span'
        )
        ret['auxiliary_node_attributes'] = spanning_auxiliary_node_attributes
        auxiliary_nodes = spanning_auxiliary_node_attributes.keys()
        if not list(auxiliary_nodes):
            raise ValueError(
                'Spanning cluster is to be detected, but no auxiliary nodes '
                'given.'
            )

        spanning_sides = list(set(spanning_auxiliary_node_attributes.values()))
        if len(spanning_sides) != 2:
            raise ValueError(
                'Spanning cluster is to be detected, but auxiliary nodes '
                'of less or more than 2 types (sides) given.'
            )

        ret['spanning_sides'] = spanning_sides
        ret['auxiliary_edge_attributes'] = nx.get_edge_attributes(
            graph, 'span'
        )

    # get subgraph on which percolation is to take place (strip off the
    # auxiliary nodes)
    if spanning_cluster:
        perc_graph = graph.subgraph(
            [
                node for node in graph.nodes_iter()
                if 'span' not in graph.node[node]
            ]
        )
    else:
        perc_graph = graph

    ret['perc_graph'] = perc_graph

    # number of nodes N
    ret['num_nodes'] = nx.number_of_nodes(perc_graph)

    # number of edges M
    ret['num_edges'] = nx.number_of_edges(perc_graph)

    return ret