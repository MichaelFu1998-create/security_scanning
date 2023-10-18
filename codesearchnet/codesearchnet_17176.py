def _microcanonical_average_spanning_cluster(has_spanning_cluster, alpha):
    r'''
    Compute the average number of runs that have a spanning cluster

    Helper function for :func:`microcanonical_averages`

    Parameters
    ----------

    has_spanning_cluster : 1-D :py:class:`numpy.ndarray` of bool
        Each entry is the ``has_spanning_cluster`` field of the output of
        :func:`sample_states`:
        An entry is ``True`` if there is a spanning cluster in that respective
        run, and ``False`` otherwise.

    alpha : float
        Significance level.

    Returns
    -------

    ret : dict
        Spanning cluster statistics

    ret['spanning_cluster'] : float
        The average relative number (Binomial proportion) of runs that have a
        spanning cluster.
        This is the Bayesian point estimate of the posterior mean, with a
        uniform prior.

    ret['spanning_cluster_ci'] : 1-D :py:class:`numpy.ndarray` of float, size 2
        The lower and upper bounds of the Binomial proportion confidence
        interval with uniform prior.

    See Also
    --------

    sample_states : spanning cluster detection

    microcanonical_averages : spanning cluster statistics

    Notes
    -----

    Averages and confidence intervals for Binomial proportions

    As Cameron [8]_ puts it, the normal approximation to the confidence
    interval for a Binomial proportion :math:`p` "suffers a *systematic*
    decline in performance (...) towards extreme values of :math:`p` near
    :math:`0` and :math:`1`, generating binomial [confidence intervals]
    with effective coverage far below the desired level." (see also
    References [6]_ and [7]_).

    A different approach to quantifying uncertainty is Bayesian inference.
    [5]_
    For :math:`n` independent Bernoulli trails with common success
    probability :math:`p`, the *likelihood* to have :math:`k` successes
    given :math:`p` is the binomial distribution

    .. math::

        P(k|p) = \binom{n}{k} p^k (1-p)^{n-k} \equiv B(a,b),

    where :math:`B(a, b)` is the *Beta distribution* with parameters
    :math:`a = k + 1` and :math:`b = n - k + 1`.
    Assuming a uniform prior :math:`P(p) = 1`, the *posterior* is [5]_

    .. math::

        P(p|k) = P(k|p)=B(a,b).

    A point estimate is the posterior mean

    .. math::

        \bar{p} = \frac{k+1}{n+2}

    with the :math:`1 - \alpha` credible interval :math:`(p_l, p_u)` given
    by

    .. math::

        \int_0^{p_l} dp B(a,b) = \int_{p_u}^1 dp B(a,b) = \frac{\alpha}{2}.

    References
    ----------

    .. [5] Wasserman, L. All of Statistics (Springer New York, 2004),
       `doi:10.1007/978-0-387-21736-9 <http://dx.doi.org/10.1007/978-0-387-21736-9>`_.

    .. [6] DasGupta, A., Cai, T. T. & Brown, L. D. Interval Estimation for a
       Binomial Proportion. Statistical Science 16, 101-133 (2001).
       `doi:10.1214/ss/1009213286 <http://dx.doi.org/10.1214/ss/1009213286>`_.

    .. [7] Agresti, A. & Coull, B. A. Approximate is Better than "Exact" for
       Interval Estimation of Binomial Proportions. The American Statistician
       52, 119-126 (1998),
       `doi:10.2307/2685469 <http://dx.doi.org/10.2307/2685469>`_.

    .. [8] Cameron, E. On the Estimation of Confidence Intervals for Binomial
       Population Proportions in Astronomy: The Simplicity and Superiority of
       the Bayesian Approach. Publications of the Astronomical Society of
       Australia 28, 128-139 (2011),
       `doi:10.1071/as10046 <http://dx.doi.org/10.1071/as10046>`_.

    '''

    ret = dict()
    runs = has_spanning_cluster.size

    # Bayesian posterior mean for Binomial proportion (uniform prior)
    k = has_spanning_cluster.sum(dtype=np.float)
    ret['spanning_cluster'] = (
        (k + 1) / (runs + 2)
    )

    # Bayesian credible interval for Binomial proportion (uniform
    # prior)
    ret['spanning_cluster_ci'] = scipy.stats.beta.ppf(
        [alpha / 2, 1 - alpha / 2], k + 1, runs - k + 1
    )

    return ret