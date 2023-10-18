def minimal_random_graph(num_vertices, seed=None, **kwargs):
    """Creates a connected graph with random vertex locations.

    Parameters
    ----------
    num_vertices : int
        The number of vertices in the graph.
    seed : int (optional)
        An integer used to initialize numpy's psuedorandom number
        generators.
    **kwargs :
        Unused.

    Returns
    -------
    :class:`.QueueNetworkDiGraph`
        A graph with a ``pos`` vertex property for each vertex's
        position.

    Notes
    -----
    This function first places ``num_vertices`` points in the unit square
    randomly (using the uniform distribution). Then, for every vertex
    ``v``, all other vertices with Euclidean distance less or equal to
    ``r`` are connect by an edge --- where ``r`` is the smallest number
    such that the graph ends up connected.
    """
    if isinstance(seed, numbers.Integral):
        np.random.seed(seed)

    points = np.random.random((num_vertices, 2)) * 10
    edges = []

    for k in range(num_vertices - 1):
        for j in range(k + 1, num_vertices):
            v = points[k] - points[j]
            edges.append((k, j, v[0]**2 + v[1]**2))

    mytype = [('n1', int), ('n2', int), ('distance', np.float)]
    edges = np.array(edges, dtype=mytype)
    edges = np.sort(edges, order='distance')
    unionF = UnionFind([k for k in range(num_vertices)])

    g = nx.Graph()

    for n1, n2, dummy in edges:
        unionF.union(n1, n2)
        g.add_edge(n1, n2)
        if unionF.nClusters == 1:
            break

    pos = {j: p for j, p in enumerate(points)}
    g = QueueNetworkDiGraph(g.to_directed())
    g.set_pos(pos)
    return g