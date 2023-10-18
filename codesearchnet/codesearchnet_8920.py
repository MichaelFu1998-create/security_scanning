def generate_random_graph(num_vertices=250, prob_loop=0.5, **kwargs):
    """Creates a random graph where the edges have different types.

    This method calls :func:`.minimal_random_graph`, and then adds
    a loop to each vertex with ``prob_loop`` probability. It then
    calls :func:`.set_types_random` on the resulting graph.

    Parameters
    ----------
    num_vertices : int (optional, default: 250)
        The number of vertices in the graph.
    prob_loop : float (optional, default: 0.5)
        The probability that a loop gets added to a vertex.
    **kwargs :
        Any parameters to send to :func:`.minimal_random_graph` or
        :func:`.set_types_random`.

    Returns
    -------
    :class:`.QueueNetworkDiGraph`
        A graph with the position of the vertex set as a property.
        The position property is called ``pos``. Also, the ``edge_type``
        edge property is set for each edge.

    Examples
    --------
    The following generates a directed graph with 50 vertices where half
    the edges are type 1 and 1/4th are type 2 and 1/4th are type 3:

    >>> import queueing_tool as qt
    >>> pTypes = {1: 0.5, 2: 0.25, 3: 0.25}
    >>> g = qt.generate_random_graph(100, proportions=pTypes, seed=17)
    >>> non_loops = [e for e in g.edges() if e[0] != e[1]]
    >>> p1 = np.sum([g.ep(e, 'edge_type') == 1 for e in non_loops])
    >>> float(p1) / len(non_loops) # doctest: +ELLIPSIS
    0.486...
    >>> p2 = np.sum([g.ep(e, 'edge_type') == 2 for e in non_loops])
    >>> float(p2) / len(non_loops) # doctest: +ELLIPSIS
    0.249...
    >>> p3 = np.sum([g.ep(e, 'edge_type') == 3 for e in non_loops])
    >>> float(p3) / len(non_loops) # doctest: +ELLIPSIS
    0.264...

    To make an undirected graph with 25 vertices where there are 4
    different edge types with random proportions:

    >>> p = np.random.rand(4)
    >>> p = p / sum(p)
    >>> p = {k + 1: p[k] for k in range(4)}
    >>> g = qt.generate_random_graph(num_vertices=25, is_directed=False, proportions=p)

    Note that none of the edge types in the above example are 0. It is
    recommended use edge type indices starting at 1, since 0 is
    typically used for terminal edges.
    """
    g = minimal_random_graph(num_vertices, **kwargs)
    for v in g.nodes():
        e = (v, v)
        if not g.is_edge(e):
            if np.random.uniform() < prob_loop:
                g.add_edge(*e)
    g = set_types_random(g, **kwargs)
    return g