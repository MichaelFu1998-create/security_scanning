def generate_pagerank_graph(num_vertices=250, **kwargs):
    """Creates a random graph where the vertex types are
    selected using their pagerank.

    Calls :func:`.minimal_random_graph` and then
    :func:`.set_types_rank` where the ``rank`` keyword argument
    is given by :func:`networkx.pagerank`.

    Parameters
    ----------
    num_vertices : int (optional, the default is 250)
        The number of vertices in the graph.
    **kwargs :
        Any parameters to send to :func:`.minimal_random_graph` or
        :func:`.set_types_rank`.

    Returns
    -------
    :class:`.QueueNetworkDiGraph`
        A graph with a ``pos`` vertex property and the ``edge_type``
        edge property.

    Notes
    -----
    This function sets the edge types of a graph to be either 1, 2, or
    3. It sets the vertices to type 2 by selecting the top
    ``pType2 * g.number_of_nodes()`` vertices given by the
    :func:`~networkx.pagerank` of the graph. A loop is added
    to all vertices identified this way (if one does not exist
    already). It then randomly sets vertices close to the type 2
    vertices as type 3, and adds loops to these vertices as well. These
    loops then have edge types that correspond to the vertices type.
    The rest of the edges are set to type 1.
    """
    g = minimal_random_graph(num_vertices, **kwargs)
    r = np.zeros(num_vertices)
    for k, pr in nx.pagerank(g).items():
        r[k] = pr
    g = set_types_rank(g, rank=r, **kwargs)
    return g