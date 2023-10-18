def _microcanonical_average_moments(moments, alpha):
    """
    Compute the average moments of the cluster size distributions

    Helper function for :func:`microcanonical_averages`

    Parameters
    ----------

    moments : 2-D :py:class:`numpy.ndarray` of int
        ``moments.shape[1] == 5`.
        Each array ``moments[r, :]`` is the ``moments`` field of the output of
        :func:`sample_states`:
        The ``k``-th entry is the ``k``-th raw moment of the (absolute) cluster
        size distribution.

    alpha: float
        Significance level.

    Returns
    -------

    ret : dict
        Moment statistics

    ret['moments'] : 1-D :py:class:`numpy.ndarray` of float, size 5
        The ``k``-th entry is the average ``k``-th raw moment of the (absolute)
        cluster size distribution, with ``k`` ranging from ``0`` to ``4``.

    ret['moments_ci'] : 2-D :py:class:`numpy.ndarray` of float, shape (5,2)
        ``ret['moments_ci'][k]`` are the lower and upper bounds of the normal
        confidence interval of the average ``k``-th raw moment of the
        (absolute) cluster size distribution, with ``k`` ranging from ``0`` to
        ``4``.

    See Also
    --------

    sample_states : computation of moments

    microcanonical_averages : moment statistics
    """

    ret = dict()
    runs = moments.shape[0]
    sqrt_n = np.sqrt(runs)

    moments_sample_mean = moments.mean(axis=0)
    ret['moments'] = moments_sample_mean

    moments_sample_std = moments.std(axis=0, ddof=1)
    ret['moments_ci'] = np.empty((5, 2))
    for k in range(5):
        if moments_sample_std[k]:
            old_settings = np.seterr(all='raise')
            ret['moments_ci'][k] = scipy.stats.t.interval(
                1 - alpha,
                df=runs - 1,
                loc=moments_sample_mean[k],
                scale=moments_sample_std[k] / sqrt_n
            )
            np.seterr(**old_settings)
        else:
            ret['moments_ci'][k] = (
                moments_sample_mean[k] * np.ones(2)
            )

    return ret