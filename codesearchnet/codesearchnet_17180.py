def spanning_1d_chain(length):
    """
    Generate a linear chain with auxiliary nodes for spanning cluster detection

    Parameters
    ----------

    length : int
       Number of nodes in the chain, excluding the auxiliary nodes.

    Returns
    -------

    networkx.Graph
       A linear chain graph with auxiliary nodes for spanning cluster detection

    See Also
    --------

    sample_states : spanning cluster detection

    """
    ret = nx.grid_graph(dim=[int(length + 2)])

    ret.node[0]['span'] = 0
    ret[0][1]['span'] = 0
    ret.node[length + 1]['span'] = 1
    ret[length][length + 1]['span'] = 1

    return ret