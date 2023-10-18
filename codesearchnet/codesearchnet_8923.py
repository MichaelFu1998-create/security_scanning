def set_types_random(g, proportions=None, loop_proportions=None, seed=None,
                     **kwargs):
    """Randomly sets ``edge_type`` (edge type) properties of the graph.

    This function randomly assigns each edge a type. The probability of
    an edge being a specific type is proscribed in the
    ``proportions``, ``loop_proportions`` variables.

    Parameters
    ----------
    g : :any:`networkx.DiGraph`, :class:`numpy.ndarray`, dict, etc.
        Any object that :any:`DiGraph<networkx.DiGraph>` accepts.
    proportions : dict (optional, default: ``{k: 0.25 for k in range(1, 4)}``)
        A dictionary of edge types and proportions, where the keys are
        the types and the values are the proportion of non-loop edges
        that are expected to be of that type. The values can must sum
        to one.
    loop_proportions : dict (optional, default: ``{k: 0.25 for k in range(4)}``)
        A dictionary of edge types and proportions, where the keys are
        the types and the values are the proportion of loop edges
        that are expected to be of that type. The values can must sum
        to one.
    seed : int (optional)
        An integer used to initialize numpy's psuedorandom number
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
        made into a :any:`networkx.DiGraph`.

    ValueError
        Raises a :exc:`~ValueError` if the ``pType`` values do not sum
        to one.

    Notes
    -----
    If ``pTypes`` is not explicitly specified in the arguments, then it
    defaults to four types in the graph (types 0, 1, 2, and 3). It sets
    non-loop edges to be either 1, 2, or 3 33\% chance, and loops are
    types 0, 1, 2, 3 with 25\% chance.
    """
    g = _test_graph(g)

    if isinstance(seed, numbers.Integral):
        np.random.seed(seed)

    if proportions is None:
        proportions = {k: 1. / 3 for k in range(1, 4)}

    if loop_proportions is None:
        loop_proportions = {k: 1. / 4 for k in range(4)}

    edges = [e for e in g.edges() if e[0] != e[1]]
    loops = [e for e in g.edges() if e[0] == e[1]]
    props = list(proportions.values())
    lprops = list(loop_proportions.values())

    if not np.isclose(sum(props), 1.0):
        raise ValueError("proportions values must sum to one.")
    if not np.isclose(sum(lprops), 1.0):
        raise ValueError("loop_proportions values must sum to one.")

    eTypes = {}
    types = list(proportions.keys())
    values = np.random.choice(types, size=len(edges), replace=True, p=props)

    for k, e in enumerate(edges):
        eTypes[e] = values[k]

    types = list(loop_proportions.keys())
    values = np.random.choice(types, size=len(loops), replace=True, p=lprops)

    for k, e in enumerate(loops):
        eTypes[e] = values[k]

    g.new_edge_property('edge_type')
    for e in g.edges():
        g.set_ep(e, 'edge_type', eTypes[e])

    return g