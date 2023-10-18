def remove_indirect_links(g, alg="aracne", **kwargs):
    """Apply deconvolution to a networkx graph.

    Args:
       g (networkx.Graph): Graph to apply deconvolution to
       alg (str): Algorithm to use ('aracne', 'clr', 'nd')
       kwargs (dict): extra options for algorithms

    Returns:
       networkx.Graph: graph with undirected links removed.
    """
    alg = {"aracne": aracne,
           "nd": network_deconvolution,
           "clr": clr}[alg]
    mat = np.array(nx.adjacency_matrix(g).todense())
    return nx.relabel_nodes(nx.DiGraph(alg(mat, **kwargs)),
                            {idx: i for idx, i in enumerate(list(g.nodes()))})