def single_run_arrays(spanning_cluster=True, **kwargs):
    r'''
    Generate statistics for a single run

    This is a stand-alone helper function to evolve a single sample state
    (realization) and return the cluster statistics.

    Parameters
    ----------
    spanning_cluster : bool, optional
        Whether to detect a spanning cluster or not.
        Defaults to ``True``.

    kwargs : keyword arguments
        Piped through to :func:`sample_states`

    Returns
    -------

    ret : dict
        Cluster statistics

    ret['N'] : int
        Total number of sites

    ret['M'] : int
        Total number of bonds

    ret['max_cluster_size'] : 1-D :py:class:`numpy.ndarray` of int, size ``ret['M'] + 1``
        Array of the sizes of the largest cluster (absolute number of sites) at
        the respective occupation number.

    ret['has_spanning_cluster'] : 1-D :py:class:`numpy.ndarray` of bool, size ``ret['M'] + 1``
        Array of booleans for each occupation number.
        The respective entry is ``True`` if there is a spanning cluster,
        ``False`` otherwise.
        Only exists if `spanning_cluster` argument is set to ``True``.

    ret['moments'] : 2-D :py:class:`numpy.ndarray` of int
        Array of shape ``(5, ret['M'] + 1)``.
        The ``(k, m)``-th entry is the ``k``-th raw moment of the (absolute)
        cluster size distribution, with ``k`` ranging from ``0`` to ``4``, at
        occupation number ``m``.

    See Also
    --------

    sample_states

    '''

    # initial iteration
    # we do not need a copy of the result dictionary since we copy the values
    # anyway
    kwargs['copy_result'] = False
    ret = dict()

    for n, state in enumerate(sample_states(
        spanning_cluster=spanning_cluster, **kwargs
    )):

        # merge cluster statistics
        if 'N' in ret:
            assert ret['N'] == state['N']
        else:
            ret['N'] = state['N']

        if 'M' in ret:
            assert ret['M'] == state['M']
        else:
            ret['M'] = state['M']
            number_of_states = state['M'] + 1
            max_cluster_size = np.empty(number_of_states)
            if spanning_cluster:
                has_spanning_cluster = np.empty(number_of_states, dtype=np.bool)
            moments = np.empty((5, number_of_states))

        max_cluster_size[n] = state['max_cluster_size']
        for k in range(5):
            moments[k, n] = state['moments'][k]
        if spanning_cluster:
            has_spanning_cluster[n] = state['has_spanning_cluster']

    ret['max_cluster_size'] = max_cluster_size
    ret['moments'] = moments
    if spanning_cluster:
        ret['has_spanning_cluster'] = has_spanning_cluster

    return ret