def generate_transition_matrix(g, seed=None):
    """Generates a random transition matrix for the graph ``g``.

    Parameters
    ----------
    g : :any:`networkx.DiGraph`, :class:`numpy.ndarray`, dict, etc.
        Any object that :any:`DiGraph<networkx.DiGraph>` accepts.
    seed : int (optional)
        An integer used to initialize numpy's psuedo-random number
        generator.

    Returns
    -------
    mat : :class:`~numpy.ndarray`
        Returns a transition matrix where ``mat[i, j]`` is the
        probability of transitioning from vertex ``i`` to vertex ``j``.
        If there is no edge connecting vertex ``i`` to vertex ``j``
        then ``mat[i, j] = 0``.
    """
    g = _test_graph(g)

    if isinstance(seed, numbers.Integral):
        np.random.seed(seed)

    nV = g.number_of_nodes()
    mat = np.zeros((nV, nV))

    for v in g.nodes():
        ind = [e[1] for e in sorted(g.out_edges(v))]
        deg = len(ind)
        if deg == 1:
            mat[v, ind] = 1
        elif deg > 1:
            probs = np.ceil(np.random.rand(deg) * 100) / 100.
            if np.isclose(np.sum(probs), 0):
                probs[np.random.randint(deg)] = 1

            mat[v, ind] = probs / np.sum(probs)

    return mat