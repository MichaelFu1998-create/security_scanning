def microcanonical_averages_arrays(microcanonical_averages):
    """
    Compile microcanonical averages over all iteration steps into single arrays

    Helper function to aggregate the microcanonical averages over all iteration
    steps into single arrays for further processing

    Parameters
    ----------

    microcanonical_averages : iterable
       Typically, this is the :func:`microcanonical_averages` generator

    Returns
    -------

    ret : dict
       Aggregated cluster statistics

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

    """

    ret = dict()

    for n, microcanonical_average in enumerate(microcanonical_averages):
        assert n == microcanonical_average['n']
        if n == 0:
            num_edges = microcanonical_average['M']
            num_sites = microcanonical_average['N']
            spanning_cluster = ('spanning_cluster' in microcanonical_average)
            ret['max_cluster_size'] = np.empty(num_edges + 1)
            ret['max_cluster_size_ci'] = np.empty((num_edges + 1, 2))

            if spanning_cluster:
                ret['spanning_cluster'] = np.empty(num_edges + 1)
                ret['spanning_cluster_ci'] = np.empty((num_edges + 1, 2))

            ret['moments'] = np.empty((5, num_edges + 1))
            ret['moments_ci'] = np.empty((5, num_edges + 1, 2))

        ret['max_cluster_size'][n] = microcanonical_average['max_cluster_size']
        ret['max_cluster_size_ci'][n] = (
            microcanonical_average['max_cluster_size_ci']
        )

        if spanning_cluster:
            ret['spanning_cluster'][n] = (
                microcanonical_average['spanning_cluster']
            )
            ret['spanning_cluster_ci'][n] = (
                microcanonical_average['spanning_cluster_ci']
            )

        ret['moments'][:, n] = microcanonical_average['moments']
        ret['moments_ci'][:, n] = microcanonical_average['moments_ci']

    # normalize by number of sites
    for key in ret:
        if 'spanning_cluster' in key:
            continue
        ret[key] /= num_sites

    ret['M'] = num_edges
    ret['N'] = num_sites
    return ret