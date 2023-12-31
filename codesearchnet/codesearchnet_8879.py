def graph2dict(g, return_dict_of_dict=True):
    """Takes a graph and returns an adjacency list.

    Parameters
    ----------
    g : :any:`networkx.DiGraph`, :any:`networkx.Graph`, etc.
        Any object that networkx can turn into a
        :any:`DiGraph<networkx.DiGraph>`.
    return_dict_of_dict : bool (optional, default: ``True``)
        Specifies whether this function will return a dict of dicts
        or a dict of lists.

    Returns
    -------
    adj : dict
        An adjacency representation of graph as a dictionary of
        dictionaries, where a key is the vertex index for a vertex
        ``v`` and the values are :class:`dicts<.dict>` with keys for
        the vertex index and values as edge properties.

    Examples
    --------
    >>> import queueing_tool as qt
    >>> import networkx as nx
    >>> adj = {0: [1, 2], 1: [0], 2: [0, 3], 3: [2]}
    >>> g = nx.DiGraph(adj)
    >>> qt.graph2dict(g, return_dict_of_dict=True)
    ...  # doctest: +NORMALIZE_WHITESPACE
    {0: {1: {}, 2: {}},
    1: {0: {}},
    2: {0: {}, 3: {}},
    3: {2: {}}}
    >>> qt.graph2dict(g, return_dict_of_dict=False)
    {0: [1, 2], 1: [0], 2: [0, 3], 3: [2]}
    """
    if not isinstance(g, nx.DiGraph):
        g = QueueNetworkDiGraph(g)

    dict_of_dicts = nx.to_dict_of_dicts(g)
    if return_dict_of_dict:
        return dict_of_dicts
    else:
        return {k: list(val.keys()) for k, val in dict_of_dicts.items()}