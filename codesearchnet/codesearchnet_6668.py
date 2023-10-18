def Wilson(xs, params):
    r'''Calculates the activity coefficients of each species in a mixture
    using the Wilson method, given their mole fractions, and
    dimensionless interaction parameters. Those are normally correlated with
    temperature, and need to be calculated separately.

    .. math::
        \ln \gamma_i = 1 - \ln \left(\sum_j^N \Lambda_{ij} x_j\right)
        -\sum_j^N \frac{\Lambda_{ji}x_j}{\displaystyle\sum_k^N \Lambda_{jk}x_k}

    Parameters
    ----------
    xs : list[float]
        Liquid mole fractions of each species, [-]
    params : list[list[float]]
        Dimensionless interaction parameters of each compound with each other,
        [-]

    Returns
    -------
    gammas : list[float]
        Activity coefficient for each species in the liquid mixture, [-]

    Notes
    -----
    This model needs N^2 parameters.

    The original model correlated the interaction parameters using the standard
    pure-component molar volumes of each species at 25°C, in the following form:

    .. math::
        \Lambda_{ij} = \frac{V_j}{V_i} \exp\left(\frac{-\lambda_{i,j}}{RT}\right)

    However, that form has less flexibility and offered no advantage over
    using only regressed parameters.

    Most correlations for the interaction parameters include some of the terms
    shown in the following form:

    .. math::
        \ln \Lambda_{ij} =a_{ij}+\frac{b_{ij}}{T}+c_{ij}\ln T + d_{ij}T
        + \frac{e_{ij}}{T^2} + h_{ij}{T^2}

    The Wilson model is not applicable to liquid-liquid systems.

    Examples
    --------
    Ethanol-water example, at 343.15 K and 1 MPa:

    >>> Wilson([0.252, 0.748], [[1, 0.154], [0.888, 1]])
    [1.8814926087178843, 1.1655774931125487]

    References
    ----------
    .. [1] Wilson, Grant M. "Vapor-Liquid Equilibrium. XI. A New Expression for
       the Excess Free Energy of Mixing." Journal of the American Chemical
       Society 86, no. 2 (January 1, 1964): 127-130. doi:10.1021/ja01056a002.
    .. [2] Gmehling, Jurgen, Barbel Kolbe, Michael Kleiber, and Jurgen Rarey.
       Chemical Thermodynamics for Process Simulation. 1st edition. Weinheim:
       Wiley-VCH, 2012.
    '''
    gammas = []
    cmps = range(len(xs))
    for i in cmps:
        tot1 = log(sum([params[i][j]*xs[j] for j in cmps]))
        tot2 = 0.
        for j in cmps:
            tot2 += params[j][i]*xs[j]/sum([params[j][k]*xs[k] for k in cmps])

        gamma = exp(1. - tot1 - tot2)
        gammas.append(gamma)
    return gammas