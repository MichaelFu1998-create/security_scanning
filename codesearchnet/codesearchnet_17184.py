def canonical_averages(ps, microcanonical_averages_arrays):
    """
    Compute the canonical cluster statistics from microcanonical statistics

    This is according to Newman and Ziff, Equation (2).
    Note that we also simply average the bounds of the confidence intervals
    according to this formula.

    Parameters
    ----------

    ps : iterable of float
       Each entry is a probability for which to form the canonical ensemble
       and compute the weighted statistics from the microcanonical statistics

    microcanonical_averages_arrays
       Typically the output of :func:`microcanonical_averages_arrays`

    Returns
    -------

    ret : dict
       Canonical ensemble cluster statistics

    ret['ps'] : iterable of float
        The parameter `ps`

    ret['N'] : int
        Total number of sites

    ret['M'] : int
        Total number of bonds

    ret['spanning_cluster'] : 1-D :py:class:`numpy.ndarray` of float
        The percolation probability:
        The normalized average number of runs that have a spanning cluster.

    ret['spanning_cluster_ci'] : 2-D :py:class:`numpy.ndarray` of float, size 2
        The lower and upper bounds of the percolation probability.

    ret['max_cluster_size'] : 1-D :py:class:`numpy.ndarray` of float
        The percolation strength:
        Average relative size of the largest cluster

    ret['max_cluster_size_ci'] : 2-D :py:class:`numpy.ndarray` of float
        Lower and upper bounds of the normal confidence interval of the
        percolation strength.

    ret['moments'] : 2-D :py:class:`numpy.ndarray` of float, shape (5, M + 1)
        Average raw moments of the (relative) cluster size distribution.

    ret['moments_ci'] : 3-D :py:class:`numpy.ndarray` of float, shape (5, M + 1, 2)
        Lower and upper bounds of the normal confidence interval of the raw
        moments of the (relative) cluster size distribution.

    See Also
    --------

    microcanonical_averages

    microcanonical_averages_arrays


    """

    num_sites = microcanonical_averages_arrays['N']
    num_edges = microcanonical_averages_arrays['M']
    spanning_cluster = ('spanning_cluster' in microcanonical_averages_arrays)

    ret = dict()
    ret['ps'] = ps
    ret['N'] = num_sites
    ret['M'] = num_edges

    ret['max_cluster_size'] = np.empty(ps.size)
    ret['max_cluster_size_ci'] = np.empty((ps.size, 2))

    if spanning_cluster:
        ret['spanning_cluster'] = np.empty(ps.size)
        ret['spanning_cluster_ci'] = np.empty((ps.size, 2))

    ret['moments'] = np.empty((5, ps.size))
    ret['moments_ci'] = np.empty((5, ps.size, 2))

    for p_index, p in enumerate(ps):
        binomials = _binomial_pmf(n=num_edges, p=p)

        for key, value in microcanonical_averages_arrays.items():
            if len(key) <= 1:
                continue

            if key in ['max_cluster_size', 'spanning_cluster']:
                ret[key][p_index] = np.sum(binomials * value)
            elif key in ['max_cluster_size_ci', 'spanning_cluster_ci']:
                ret[key][p_index] = np.sum(
                    np.tile(binomials, (2, 1)).T * value, axis=0
                )
            elif key == 'moments':
                ret[key][:, p_index] = np.sum(
                    np.tile(binomials, (5, 1)) * value, axis=1
                )
            elif key == 'moments_ci':
                ret[key][:, p_index] = np.sum(
                    np.rollaxis(np.tile(binomials, (5, 2, 1)), 2, 1) * value,
                    axis=1
                )
            else:
                raise NotImplementedError(
                    '{}-dimensional array'.format(value.ndim)
                )

    return ret