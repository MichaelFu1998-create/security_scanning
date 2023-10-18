def _microcanonical_average_max_cluster_size(max_cluster_size, alpha):
    """
    Compute the average size of the largest cluster

    Helper function for :func:`microcanonical_averages`

    Parameters
    ----------

    max_cluster_size : 1-D :py:class:`numpy.ndarray` of int
        Each entry is the ``max_cluster_size`` field of the output of
        :func:`sample_states`:
        The size of the largest cluster (absolute number of sites).

    alpha: float
        Significance level.

    Returns
    -------

    ret : dict
        Largest cluster statistics

    ret['max_cluster_size'] : float
        Average size of the largest cluster (absolute number of sites)

    ret['max_cluster_size_ci'] : 1-D :py:class:`numpy.ndarray` of float, size 2
        Lower and upper bounds of the normal confidence interval of the average
        size of the largest cluster (absolute number of sites)

    See Also
    --------

    sample_states : largest cluster detection

    microcanonical_averages : largest cluster statistics
    """

    ret = dict()
    runs = max_cluster_size.size
    sqrt_n = np.sqrt(runs)

    max_cluster_size_sample_mean = max_cluster_size.mean()
    ret['max_cluster_size'] = max_cluster_size_sample_mean

    max_cluster_size_sample_std = max_cluster_size.std(ddof=1)
    if max_cluster_size_sample_std:
        old_settings = np.seterr(all='raise')
        ret['max_cluster_size_ci'] = scipy.stats.t.interval(
            1 - alpha,
            df=runs - 1,
            loc=max_cluster_size_sample_mean,
            scale=max_cluster_size_sample_std / sqrt_n
        )
        np.seterr(**old_settings)
    else:
        ret['max_cluster_size_ci'] = (
            max_cluster_size_sample_mean * np.ones(2)
        )

    return ret