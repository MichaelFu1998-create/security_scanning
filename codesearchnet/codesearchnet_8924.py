def set_types_rank(g, rank, pType2=0.1, pType3=0.1, seed=None, **kwargs):
    """Creates a stylized graph. Sets edge and types using `pagerank`_.

    This function sets the edge types of a graph to be either 1, 2, or
    3. It sets the vertices to type 2 by selecting the top
    ``pType2 * g.number_of_nodes()`` vertices given by the
    :func:`~networkx.pagerank` of the graph. A loop is added
    to all vertices identified this way (if one does not exist
    already). It then randomly sets vertices close to the type 2
    vertices as type 3, and adds loops to these vertices as well. These
    loops then have edge types the correspond to the vertices type. The
    rest of the edges are set to type 1.

    .. _pagerank: http://en.wikipedia.org/wiki/PageRank

    Parameters
    ----------
    g : :any:`networkx.DiGraph`, :class:`~numpy.ndarray`, dict, etc.
        Any object that :any:`DiGraph<networkx.DiGraph>` accepts.
    rank : :class:`numpy.ndarray`
        An ordering of the vertices.
    pType2 : float (optional, default: 0.1)
        Specifies the proportion of vertices that will be of type 2.
    pType3 : float (optional, default: 0.1)
        Specifies the proportion of vertices that will be of type 3 and
        that are near pType2 vertices.
    seed : int (optional)
        An integer used to initialize numpy's psuedo-random number
        generator.
    **kwargs :
        Unused.

    Returns
    -------
    :class:`.QueueNetworkDiGraph`
        Returns the a graph with an ``edge_type`` edge property.

    Raises
    ------
    TypeError
        Raised when the parameter ``g`` is not of a type that can be
        made into a :any:`DiGraph<networkx.DiGraph>`.
    """
    g = _test_graph(g)

    if isinstance(seed, numbers.Integral):
        np.random.seed(seed)

    tmp = np.sort(np.array(rank))
    nDests = int(np.ceil(g.number_of_nodes() * pType2))
    dests = np.where(rank >= tmp[-nDests])[0]

    if 'pos' not in g.vertex_properties():
        g.set_pos()

    dest_pos = np.array([g.vp(v, 'pos') for v in dests])
    nFCQ = int(pType3 * g.number_of_nodes())
    min_g_dist = np.ones(nFCQ) * np.infty
    ind_g_dist = np.ones(nFCQ, int)

    r, theta = np.random.random(nFCQ) / 500., np.random.random(nFCQ) * 360.
    xy_pos = np.array([r * np.cos(theta), r * np.sin(theta)]).transpose()
    g_pos = xy_pos + dest_pos[np.array(np.mod(np.arange(nFCQ), nDests), int)]

    for v in g.nodes():
        if v not in dests:
            tmp = np.array([_calculate_distance(g.vp(v, 'pos'), g_pos[k, :]) for k in range(nFCQ)])
            min_g_dist = np.min((tmp, min_g_dist), 0)
            ind_g_dist[min_g_dist == tmp] = v

    ind_g_dist = np.unique(ind_g_dist)
    fcqs = set(ind_g_dist[:min(nFCQ, len(ind_g_dist))])
    dests = set(dests)
    g.new_vertex_property('loop_type')

    for v in g.nodes():
        if v in dests:
            g.set_vp(v, 'loop_type', 3)
            if not g.is_edge((v, v)):
                g.add_edge(v, v)
        elif v in fcqs:
            g.set_vp(v, 'loop_type', 2)
            if not g.is_edge((v, v)):
                g.add_edge(v, v)

    g.new_edge_property('edge_type')
    for e in g.edges():
        g.set_ep(e, 'edge_type', 1)

    for v in g.nodes():
        if g.vp(v, 'loop_type') in [2, 3]:
            e = (v, v)
            if g.vp(v, 'loop_type') == 2:
                g.set_ep(e, 'edge_type', 2)
            else:
                g.set_ep(e, 'edge_type', 3)

    return g