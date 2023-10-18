def adjacency2graph(adjacency, edge_type=None, adjust=1, **kwargs):
    """Takes an adjacency list, dict, or matrix and returns a graph.

    The purpose of this function is take an adjacency list (or matrix)
    and return a :class:`.QueueNetworkDiGraph` that can be used with a
    :class:`.QueueNetwork` instance. The Graph returned has the
    ``edge_type`` edge property set for each edge. Note that the graph may
    be altered.

    Parameters
    ----------
    adjacency : dict or :class:`~numpy.ndarray`
        An adjacency list as either a dict, or an adjacency matrix.
    adjust : int ``{1, 2}`` (optional, default: 1)
        Specifies what to do when the graph has terminal vertices
        (nodes with no out-edges). Note that if ``adjust`` is not 2
        then it is assumed to be 1. There are two choices:

        * ``adjust = 1``: A loop is added to each terminal node in the
          graph, and their ``edge_type`` of that loop is set to 0.
        * ``adjust = 2``: All edges leading to terminal nodes have
          their ``edge_type`` set to 0.

    **kwargs :
        Unused.

    Returns
    -------
    out : :any:`networkx.DiGraph`
        A directed graph with the ``edge_type`` edge property.

    Raises
    ------
    TypeError
        Is raised if ``adjacency`` is not a dict or
        :class:`~numpy.ndarray`.

    Examples
    --------
    If terminal nodes are such that all in-edges have edge type ``0``
    then nothing is changed. However, if a node is a terminal node then
    a loop is added with edge type 0.

    >>> import queueing_tool as qt
    >>> adj = {
    ...     0: {1: {}},
    ...     1: {2: {},
    ...         3: {}},
    ...     3: {0: {}}}
    >>> eTy = {0: {1: 1}, 1: {2: 2, 3: 4}, 3: {0: 1}}
    >>> # A loop will be added to vertex 2
    >>> g = qt.adjacency2graph(adj, edge_type=eTy)
    >>> ans = qt.graph2dict(g)
    >>> sorted(ans.items())     # doctest: +NORMALIZE_WHITESPACE
    [(0, {1: {'edge_type': 1}}),
     (1, {2: {'edge_type': 2}, 3: {'edge_type': 4}}), 
     (2, {2: {'edge_type': 0}}),
     (3, {0: {'edge_type': 1}})]

    You can use a dict of lists to represent the adjacency list.

    >>> adj = {0 : [1], 1: [2, 3], 3: [0]}
    >>> g = qt.adjacency2graph(adj, edge_type=eTy)
    >>> ans = qt.graph2dict(g)
    >>> sorted(ans.items())     # doctest: +NORMALIZE_WHITESPACE
    [(0, {1: {'edge_type': 1}}),
     (1, {2: {'edge_type': 2}, 3: {'edge_type': 4}}),
     (2, {2: {'edge_type': 0}}),
     (3, {0: {'edge_type': 1}})]

    Alternatively, you could have this function adjust the edges that
    lead to terminal vertices by changing their edge type to 0:

    >>> # The graph is unaltered
    >>> g = qt.adjacency2graph(adj, edge_type=eTy, adjust=2)
    >>> ans = qt.graph2dict(g)
    >>> sorted(ans.items())     # doctest: +NORMALIZE_WHITESPACE
    [(0, {1: {'edge_type': 1}}),
     (1, {2: {'edge_type': 0}, 3: {'edge_type': 4}}),
     (2, {}),
     (3, {0: {'edge_type': 1}})]
    """

    if isinstance(adjacency, np.ndarray):
        adjacency = _matrix2dict(adjacency)
    elif isinstance(adjacency, dict):
        adjacency = _dict2dict(adjacency)
    else:
        msg = ("If the adjacency parameter is supplied it must be a "
               "dict, or a numpy.ndarray.")
        raise TypeError(msg)

    if edge_type is None:
        edge_type = {}
    else:
        if isinstance(edge_type, np.ndarray):
            edge_type = _matrix2dict(edge_type, etype=True)
        elif isinstance(edge_type, dict):
            edge_type = _dict2dict(edge_type)

    for u, ty in edge_type.items():
        for v, et in ty.items():
            adjacency[u][v]['edge_type'] = et

    g = nx.from_dict_of_dicts(adjacency, create_using=nx.DiGraph())
    adjacency = nx.to_dict_of_dicts(g)
    adjacency = _adjacency_adjust(adjacency, adjust, True)

    return nx.from_dict_of_dicts(adjacency, create_using=nx.DiGraph())