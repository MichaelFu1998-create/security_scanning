def bernoulli_sample(
    offset,
    G,
    heritability=0.5,
    causal_variants=None,
    causal_variance=0,
    random_state=None,
):
    r"""Bernoulli likelihood sampling.

    Sample according to

    .. math::

        \mathbf y \sim \prod_{i=1}^n
        \text{Bernoulli}(\mu_i = \text{logit}(z_i))
        \mathcal N(~ o \mathbf 1 + \mathbf a^\intercal \boldsymbol\alpha;
        ~ (h^2 - v_c)\mathrm G^\intercal\mathrm G +
        (1-h^2-v_c)\mathrm I ~)

    using the canonical Logit link function to define the conditional Bernoulli
    mean :math:`\mu_i`.

    The causal :math:`\mathbf a` covariates and the corresponding effect-sizes
    are randomly draw according to the following idea. The ``causal_variants``,
    if given, are first mean-zero and std-one normalized and then having
    its elements divided by the squared-root the the number of variances::

        causal_variants = _stdnorm(causal_variants, axis=0)
        causal_variants /= sqrt(causal_variants.shape[1])

    The causal effect-sizes :math:`\boldsymbol\alpha` are draw from
    :math:`\{-1, +1\}` and subsequently normalized for mean-zero and std-one""

    Parameters
    ----------
    random_state : random_state
        Set the initial random state.

    Example
    -------

    .. doctest::

        >>> from glimix_core.random import bernoulli_sample
        >>> from numpy.random import RandomState
        >>> offset = 5
        >>> G = [[1, -1], [2, 1]]
        >>> bernoulli_sample(offset, G, random_state=RandomState(0))
        array([1., 1.])
    """
    link = LogitLink()
    mean, cov = _mean_cov(
        offset, G, heritability, causal_variants, causal_variance, random_state
    )
    lik = BernoulliProdLik(link)
    sampler = GGPSampler(lik, mean, cov)

    return sampler.sample(random_state)