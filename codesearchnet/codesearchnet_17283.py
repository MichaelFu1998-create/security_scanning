def bond_sample_states(
    perc_graph, num_nodes, num_edges, seed, spanning_cluster=True,
    auxiliary_node_attributes=None, auxiliary_edge_attributes=None,
    spanning_sides=None,
    **kwargs
):
    '''
    Generate successive sample states of the bond percolation model

    This is a :ref:`generator function <python:tut-generators>` to successively
    add one edge at a time from the graph to the percolation model.
    At each iteration, it calculates and returns the cluster statistics.
    CAUTION: it returns a reference to the internal array, not a copy.

    Parameters
    ----------
    perc_graph : networkx.Graph
        The substrate graph on which percolation is to take place

    num_nodes : int
        Number ``N`` of sites in the graph

    num_edges : int
        Number ``M`` of bonds in the graph

    seed : {None, int, array_like}
        Random seed initializing the pseudo-random number generator.
        Piped through to `numpy.random.RandomState` constructor.

    spanning_cluster : bool, optional
        Whether to detect a spanning cluster or not.
        Defaults to ``True``.

    auxiliary_node_attributes : optional
        Return value of ``networkx.get_node_attributes(graph, 'span')``

    auxiliary_edge_attributes : optional
        Return value of ``networkx.get_edge_attributes(graph, 'span')``

    spanning_sides : list, optional
        List of keys (attribute values) of the two sides of the auxiliary
        nodes.
        Return value of ``list(set(auxiliary_node_attributes.values()))``

    Yields
    ------
    ret : ndarray
        Structured array with dtype ``dtype=[('has_spanning_cluster', 'bool'),
        ('max_cluster_size', 'uint32'), ('moments', 'int64', 5)]``

    ret['n'] : ndarray of int
        The number of bonds added at the particular iteration

    ret['edge'] : ndarray of int
        The index of the edge added at the particular iteration
        Note that in the first step, when ``ret['n'] == 0``, this value is
        undefined!

    ret['has_spanning_cluster'] : ndarray of bool
        ``True`` if there is a spanning cluster, ``False`` otherwise.
        Only exists if `spanning_cluster` argument is set to ``True``.

    ret['max_cluster_size'] : int
        Size of the largest cluster (absolute number of sites)

    ret['moments'] : 1-D :py:class:`numpy.ndarray` of int
        Array of size ``5``.
        The ``k``-th entry is the ``k``-th raw moment of the (absolute) cluster
        size distribution, with ``k`` ranging from ``0`` to ``4``.

    Raises
    ------
    ValueError
        If `spanning_cluster` is ``True``, but `graph` does not contain any
        auxiliary nodes to detect spanning clusters.

    See also
    --------

    numpy.random.RandomState

    microcanonical_statistics_dtype

    Notes
    -----
    Iterating through this generator is a single run of the Newman-Ziff
    algorithm. [12]_
    The first iteration yields the trivial state with :math:`n = 0` occupied
    bonds.

    Spanning cluster

        In order to detect a spanning cluster, `graph` needs to contain
        auxiliary nodes and edges, cf. Reference [12]_, Figure 6.
        The auxiliary nodes and edges have the ``'span'`` `attribute
        <http://networkx.github.io/documentation/latest/tutorial/tutorial.html#node-attributes>`_.
        The value is either ``0`` or ``1``, distinguishing the two sides of the
        graph to span.

    Raw moments of the cluster size distribution

        The :math:`k`-th raw moment of the (absolute) cluster size distribution
        is :math:`\sum_s' s^k N_s`, where :math:`s` is the cluster size and
        :math:`N_s` is the number of clusters of size :math:`s`. [13]_
        The primed sum :math:`\sum'` signifies that the largest cluster is
        excluded from the sum. [14]_

    References
    ----------
    .. [12] Newman, M. E. J. & Ziff, R. M. Fast monte carlo algorithm for site
        or bond percolation. Physical Review E 64, 016706+ (2001),
        `doi:10.1103/physreve.64.016706 <http://dx.doi.org/10.1103/physreve.64.016706>`_.

    .. [13] Stauffer, D. & Aharony, A. Introduction to Percolation Theory (Taylor &
       Francis, London, 1994), second edn.

    .. [14] Binder, K. & Heermann, D. W. Monte Carlo Simulation in Statistical
       Physics (Springer, Berlin, Heidelberg, 2010),
       `doi:10.1007/978-3-642-03163-2 <http://dx.doi.org/10.1007/978-3-642-03163-2>`_.
    '''

    # construct random number generator
    rng = np.random.RandomState(seed=seed)

    if spanning_cluster:
        if len(spanning_sides) != 2:
            raise ValueError(
                'Spanning cluster is to be detected, but auxiliary nodes '
                'of less or more than 2 types (sides) given.'
            )

    # get a list of edges for easy access in later iterations
    perc_edges = perc_graph.edges()
    perm_edges = rng.permutation(num_edges)

    # initial iteration: no edges added yet (n == 0)
    ret = np.empty(
        1, dtype=microcanonical_statistics_dtype(spanning_cluster)
    )

    ret['n'] = 0
    ret['max_cluster_size'] = 1
    ret['moments'] = np.ones(5, dtype='uint64') * (num_nodes - 1)

    if spanning_cluster:
        ret['has_spanning_cluster'] = False

    # yield cluster statistics for n == 0
    yield ret

    # set up disjoint set (union-find) data structure
    ds = nx.utils.union_find.UnionFind()
    if spanning_cluster:
        ds_spanning = nx.utils.union_find.UnionFind()

        # merge all auxiliary nodes for each side
        side_roots = dict()
        for side in spanning_sides:
            nodes = [
                node for (node, node_side) in auxiliary_node_attributes.items()
                if node_side is side
            ]
            ds_spanning.union(*nodes)
            side_roots[side] = ds_spanning[nodes[0]]

        for (edge, edge_side) in auxiliary_edge_attributes.items():
            ds_spanning.union(side_roots[edge_side], *edge)

        side_roots = [
            ds_spanning[side_root] for side_root in side_roots.values()
        ]

    # get first node
    max_cluster_root = next(perc_graph.nodes_iter())

    # loop over all edges (n == 1..M)
    for n in range(num_edges):

        ret['n'] += 1

        # draw new edge from permutation
        edge_index = perm_edges[n]
        edge = perc_edges[edge_index]
        ret['edge'] = edge_index

        # find roots and weights
        roots = [
            ds[node] for node in edge
        ]
        weights = [
            ds.weights[root] for root in roots
        ]

        if roots[0] is not roots[1]:
            # not same cluster: union!
            ds.union(*roots)
            if spanning_cluster:
                ds_spanning.union(*roots)

                ret['has_spanning_cluster'] = (
                    ds_spanning[side_roots[0]] == ds_spanning[side_roots[1]]
                )

            # find new root and weight
            root = ds[edge[0]]
            weight = ds.weights[root]

            # moments and maximum cluster size

            # deduct the previous sub-maximum clusters from moments
            for i in [0, 1]:
                if roots[i] is max_cluster_root:
                    continue
                ret['moments'] -= weights[i] ** np.arange(5, dtype='uint64')

            if max_cluster_root in roots:
                # merged with maximum cluster
                max_cluster_root = root
                ret['max_cluster_size'] = weight
            else:
                # merged previously sub-maximum clusters
                if ret['max_cluster_size'] >= weight:
                    # previously largest cluster remains largest cluster
                    # add merged cluster to moments
                    ret['moments'] += weight ** np.arange(5, dtype='uint64')
                else:
                    # merged cluster overtook previously largest cluster
                    # add previously largest cluster to moments
                    max_cluster_root = root
                    ret['moments'] += ret['max_cluster_size'] ** np.arange(
                        5, dtype='uint64'
                    )
                    ret['max_cluster_size'] = weight

        yield ret