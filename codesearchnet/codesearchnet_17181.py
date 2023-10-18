def spanning_2d_grid(length):
    """
    Generate a square lattice with auxiliary nodes for spanning detection

    Parameters
    ----------

    length : int
       Number of nodes in one dimension, excluding the auxiliary nodes.

    Returns
    -------

    networkx.Graph
       A square lattice graph with auxiliary nodes for spanning cluster
       detection

    See Also
    --------

    sample_states : spanning cluster detection

    """
    ret = nx.grid_2d_graph(length + 2, length)

    for i in range(length):
        # side 0
        ret.node[(0, i)]['span'] = 0
        ret[(0, i)][(1, i)]['span'] = 0

        # side 1
        ret.node[(length + 1, i)]['span'] = 1
        ret[(length + 1, i)][(length, i)]['span'] = 1

    return ret