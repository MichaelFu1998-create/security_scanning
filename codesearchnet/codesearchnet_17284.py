def bond_microcanonical_statistics(
    perc_graph, num_nodes, num_edges, seed,
    spanning_cluster=True,
    auxiliary_node_attributes=None, auxiliary_edge_attributes=None,
    spanning_sides=None,
    **kwargs
):
    """
    Evolve a single run over all microstates (bond occupation numbers)

    Return the cluster statistics for each microstate

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
        Value of ``networkx.get_node_attributes(graph, 'span')``

    auxiliary_edge_attributes : optional
        Value of ``networkx.get_edge_attributes(graph, 'span')``

    spanning_sides : list, optional
        List of keys (attribute values) of the two sides of the auxiliary
        nodes.
        Return value of ``list(set(auxiliary_node_attributes.values()))``

    Returns
    -------
    ret : ndarray of size ``num_edges + 1``
        Structured array with dtype ``dtype=[('has_spanning_cluster', 'bool'),
        ('max_cluster_size', 'uint32'), ('moments', 'uint64', 5)]``

    ret['n'] : ndarray of int
        The number of bonds added at the particular iteration

    ret['edge'] : ndarray of int
        The index of the edge added at the particular iteration.
        Note that ``ret['edge'][0]`` is undefined!

    ret['has_spanning_cluster'] : ndarray of bool
        ``True`` if there is a spanning cluster, ``False`` otherwise.
        Only exists if `spanning_cluster` argument is set to ``True``.

    ret['max_cluster_size'] : int
        Size of the largest cluster (absolute number of sites)

    ret['moments'] : 2-D :py:class:`numpy.ndarray` of int
        Array of shape ``(num_edges + 1, 5)``.
        The ``k``-th entry is the ``k``-th raw moment of the (absolute) cluster
        size distribution, with ``k`` ranging from ``0`` to ``4``.

    See also
    --------

    bond_sample_states
    microcanonical_statistics_dtype

    numpy.random.RandomState

    """

    # initialize generator
    sample_states = bond_sample_states(
        perc_graph=perc_graph,
        num_nodes=num_nodes,
        num_edges=num_edges,
        seed=seed,
        spanning_cluster=spanning_cluster,
        auxiliary_node_attributes=auxiliary_node_attributes,
        auxiliary_edge_attributes=auxiliary_edge_attributes,
        spanning_sides=spanning_sides,
    )

    # get cluster statistics over all microstates
    return np.fromiter(
        sample_states,
        dtype=microcanonical_statistics_dtype(spanning_cluster),
        count=num_edges + 1
    )