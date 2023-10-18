def add_edge_lengths(g):
    """Add add the edge lengths as a :any:`DiGraph<networkx.DiGraph>`
    for the graph.

    Uses the ``pos`` vertex property to get the location of each
    vertex. These are then used to calculate the length of an edge
    between two vertices.

    Parameters
    ----------
    g : :any:`networkx.DiGraph`, :class:`numpy.ndarray`, dict, \
        ``None``, etc.
        Any object that networkx can turn into a
        :any:`DiGraph<networkx.DiGraph>`

    Returns
    -------
    :class:`.QueueNetworkDiGraph`
        Returns the a graph with the ``edge_length`` edge property.

    Raises
    ------
    TypeError
        Raised when the parameter ``g`` is not of a type that can be
        made into a :any:`networkx.DiGraph`.

    """
    g = _test_graph(g)
    g.new_edge_property('edge_length')

    for e in g.edges():
        latlon1 = g.vp(e[1], 'pos')
        latlon2 = g.vp(e[0], 'pos')
        g.set_ep(e, 'edge_length', np.round(_calculate_distance(latlon1, latlon2), 3))

    return g