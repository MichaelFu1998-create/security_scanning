def poisson_sample(
    offset,
    G,
    heritability=0.5,
    causal_variants=None,
    causal_variance=0,
    random_state=None,
):
    """Poisson likelihood sampling.

    Parameters
    ----------
    random_state : random_state
        Set the initial random state.

    Example
    -------

    .. doctest::

        >>> from glimix_core.random import poisson_sample
        >>> from numpy.random import RandomState
        >>> offset = -0.5
        >>> G = [[0.5, -1], [2, 1]]
        >>> poisson_sample(offset, G, random_state=RandomState(0))
        array([0, 6])
    """
    mean, cov = _mean_cov(
        offset, G, heritability, causal_variants, causal_variance, random_state
    )
    link = LogLink()
    lik = PoissonProdLik(link)
    sampler = GGPSampler(lik, mean, cov)

    return sampler.sample(random_state)