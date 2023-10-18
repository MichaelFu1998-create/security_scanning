def microcanonical_averages(
    graph, runs=40, spanning_cluster=True, model='bond', alpha=alpha_1sigma,
    copy_result=True
):
    r'''
    Generate successive microcanonical percolation ensemble averages

    This is a :ref:`generator function <python:tut-generators>` to successively
    add one edge at a time from the graph to the percolation model for a number
    of independent runs in parallel.
    At each iteration, it calculates and returns the averaged cluster
    statistics.

    Parameters
    ----------
    graph : networkx.Graph
        The substrate graph on which percolation is to take place

    runs : int, optional
        Number of independent runs.
        Defaults to ``40``.

    spanning_cluster : bool, optional
        Defaults to ``True``.

    model : str, optional
        The percolation model (either ``'bond'`` or ``'site'``).
        Defaults to ``'bond'``.

        .. note:: Other models than ``'bond'`` are not supported yet.

    alpha: float, optional
        Significance level.
        Defaults to 1 sigma of the normal distribution.
        ``1 - alpha`` is the confidence level.

    copy_result : bool, optional
        Whether to return a copy or a reference to the result dictionary.
        Defaults to ``True``.

    Yields
    ------
    ret : dict
        Cluster statistics

    ret['n'] : int
        Number of occupied bonds

    ret['N'] : int
        Total number of sites

    ret['M'] : int
        Total number of bonds

    ret['spanning_cluster'] : float
        The average number (Binomial proportion) of runs that have a spanning
        cluster.
        This is the Bayesian point estimate of the posterior mean, with a
        uniform prior.
        Only exists if `spanning_cluster` is set to ``True``.

    ret['spanning_cluster_ci'] : 1-D :py:class:`numpy.ndarray` of float, size 2
        The lower and upper bounds of the Binomial proportion confidence
        interval with uniform prior.
        Only exists if `spanning_cluster` is set to ``True``.

    ret['max_cluster_size'] : float
        Average size of the largest cluster (absolute number of sites)

    ret['max_cluster_size_ci'] : 1-D :py:class:`numpy.ndarray` of float, size 2
        Lower and upper bounds of the normal confidence interval of the average
        size of the largest cluster (absolute number of sites)

    ret['moments'] : 1-D :py:class:`numpy.ndarray` of float, size 5
        The ``k``-th entry is the average ``k``-th raw moment of the (absolute)
        cluster size distribution, with ``k`` ranging from ``0`` to ``4``.

    ret['moments_ci'] : 2-D :py:class:`numpy.ndarray` of float, shape (5,2)
        ``ret['moments_ci'][k]`` are the lower and upper bounds of the normal
        confidence interval of the average ``k``-th raw moment of the
        (absolute) cluster size distribution, with ``k`` ranging from ``0`` to
        ``4``.

    Raises
    ------
    ValueError
        If `runs` is not a positive integer

    ValueError
        If `alpha` is not a float in the interval (0, 1)

    See also
    --------

    sample_states

    percolate.percolate._microcanonical_average_spanning_cluster

    percolate.percolate._microcanonical_average_max_cluster_size

    Notes
    -----
    Iterating through this generator corresponds to several parallel runs of
    the Newman-Ziff algorithm.
    Each iteration yields a microcanonical percolation ensemble for the number
    :math:`n` of occupied bonds. [9]_
    The first iteration yields the trivial microcanonical percolation ensemble
    with :math:`n = 0` occupied bonds.

    Spanning cluster

        .. seealso:: :py:func:`sample_states`

    Raw moments of the cluster size distribution

        .. seealso:: :py:func:`sample_states`


    References
    ----------
    .. [9] Newman, M. E. J. & Ziff, R. M. Fast monte carlo algorithm for site
        or bond percolation. Physical Review E 64, 016706+ (2001),
        `doi:10.1103/physreve.64.016706 <http://dx.doi.org/10.1103/physreve.64.016706>`_.

    '''

    try:
        runs = int(runs)
    except:
        raise ValueError("runs needs to be a positive integer")

    if runs <= 0:
        raise ValueError("runs needs to be a positive integer")

    try:
        alpha = float(alpha)
    except:
        raise ValueError("alpha needs to be a float in the interval (0, 1)")

    if alpha <= 0.0 or alpha >= 1.0:
        raise ValueError("alpha needs to be a float in the interval (0, 1)")

    # initial iteration
    # we do not need a copy of the result dictionary since we copy the values
    # anyway
    run_iterators = [
        sample_states(
            graph, spanning_cluster=spanning_cluster, model=model,
            copy_result=False
        )
        for _ in range(runs)
    ]

    ret = dict()
    for microcanonical_ensemble in zip(*run_iterators):
        # merge cluster statistics
        ret['n'] = microcanonical_ensemble[0]['n']
        ret['N'] = microcanonical_ensemble[0]['N']
        ret['M'] = microcanonical_ensemble[0]['M']

        max_cluster_size = np.empty(runs)
        moments = np.empty((runs, 5))
        if spanning_cluster:
            has_spanning_cluster = np.empty(runs)

        for r, state in enumerate(microcanonical_ensemble):
            assert state['n'] == ret['n']
            assert state['N'] == ret['N']
            assert state['M'] == ret['M']
            max_cluster_size[r] = state['max_cluster_size']
            moments[r] = state['moments']
            if spanning_cluster:
                has_spanning_cluster[r] = state['has_spanning_cluster']

        ret.update(_microcanonical_average_max_cluster_size(
            max_cluster_size, alpha
        ))

        ret.update(_microcanonical_average_moments(moments, alpha))

        if spanning_cluster:
            ret.update(_microcanonical_average_spanning_cluster(
                has_spanning_cluster, alpha
            ))

        if copy_result:
            yield copy.deepcopy(ret)
        else:
            yield ret