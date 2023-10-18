def UNIQUAC(xs, rs, qs, taus):
    r'''Calculates the activity coefficients of each species in a mixture
    using the Universal quasi-chemical (UNIQUAC) equation, given their mole
    fractions, `rs`, `qs`, and dimensionless interaction parameters. The
    interaction parameters are normally correlated with temperature, and need
    to be calculated separately.

    .. math::
        \ln \gamma_i = \ln \frac{\Phi_i}{x_i} + \frac{z}{2} q_i \ln
        \frac{\theta_i}{\Phi_i}+ l_i - \frac{\Phi_i}{x_i}\sum_j^N x_j l_j
        - q_i \ln\left( \sum_j^N \theta_j \tau_{ji}\right)+ q_i - q_i\sum_j^N
        \frac{\theta_j \tau_{ij}}{\sum_k^N \theta_k \tau_{kj}}

        \theta_i = \frac{x_i q_i}{\displaystyle\sum_{j=1}^{n} x_j q_j}

         \Phi_i = \frac{x_i r_i}{\displaystyle\sum_{j=1}^{n} x_j r_j}

         l_i = \frac{z}{2}(r_i - q_i) - (r_i - 1)

    Parameters
    ----------
    xs : list[float]
        Liquid mole fractions of each species, [-]
    rs : list[float]
        Van der Waals volume parameters for each species, [-]
    qs : list[float]
        Surface area parameters for each species, [-]
    taus : list[list[float]]
        Dimensionless interaction parameters of each compound with each other,
        [-]

    Returns
    -------
    gammas : list[float]
        Activity coefficient for each species in the liquid mixture, [-]

    Notes
    -----
    This model needs N^2 parameters.

    The original expression for the interaction parameters is as follows:

    .. math::
        \tau_{ji} = \exp\left(\frac{-\Delta u_{ij}}{RT}\right)

    However, it is seldom used. Most correlations for the interaction
    parameters include some of the terms shown in the following form:

    .. math::
        \ln \tau{ij} =a_{ij}+\frac{b_{ij}}{T}+c_{ij}\ln T + d_{ij}T
        + \frac{e_{ij}}{T^2}

    This model is recast in a slightly more computationally efficient way in
    [2]_, as shown below:

    .. math::
        \ln \gamma_i = \ln \gamma_i^{res} + \ln \gamma_i^{comb}

        \ln \gamma_i^{res} = q_i \left(1 - \ln\frac{\sum_j^N q_j x_j \tau_{ji}}
        {\sum_j^N q_j x_j}- \sum_j \frac{q_k x_j \tau_{ij}}{\sum_k q_k x_k
        \tau_{kj}}\right)

        \ln \gamma_i^{comb} = (1 - V_i + \ln V_i) - \frac{z}{2}q_i\left(1 -
        \frac{V_i}{F_i} + \ln \frac{V_i}{F_i}\right)

        V_i = \frac{r_i}{\sum_j^N r_j x_j}

        F_i = \frac{q_i}{\sum_j q_j x_j}

    Examples
    --------
    Ethanol-water example, at 343.15 K and 1 MPa:

    >>> UNIQUAC(xs=[0.252, 0.748], rs=[2.1055, 0.9200], qs=[1.972, 1.400],
    ... taus=[[1.0, 1.0919744384510301], [0.37452902779205477, 1.0]])
    [2.35875137797083, 1.2442093415968987]

    References
    ----------
    .. [1] Abrams, Denis S., and John M. Prausnitz. "Statistical Thermodynamics
       of Liquid Mixtures: A New Expression for the Excess Gibbs Energy of
       Partly or Completely Miscible Systems." AIChE Journal 21, no. 1 (January
       1, 1975): 116-28. doi:10.1002/aic.690210115.
    .. [2] Gmehling, Jurgen, Barbel Kolbe, Michael Kleiber, and Jurgen Rarey.
       Chemical Thermodynamics for Process Simulation. 1st edition. Weinheim:
       Wiley-VCH, 2012.
    .. [3] Maurer, G., and J. M. Prausnitz. "On the Derivation and Extension of
       the Uniquac Equation." Fluid Phase Equilibria 2, no. 2 (January 1,
       1978): 91-99. doi:10.1016/0378-3812(78)85002-X.
    '''
    cmps = range(len(xs))
    rsxs = sum([rs[i]*xs[i] for i in cmps])
    phis = [rs[i]*xs[i]/rsxs for i in cmps]
    qsxs = sum([qs[i]*xs[i] for i in cmps])
    vs = [qs[i]*xs[i]/qsxs for i in cmps]

    Ss = [sum([vs[j]*taus[j][i] for j in cmps]) for i in cmps]

    loggammacs = [log(phis[i]/xs[i]) + 1 - phis[i]/xs[i]
    - 5*qs[i]*(log(phis[i]/vs[i]) + 1 - phis[i]/vs[i]) for i in cmps]

    loggammars = [qs[i]*(1 - log(Ss[i]) - sum([taus[i][j]*vs[j]/Ss[j]
                  for j in cmps])) for i in cmps]

    return [exp(loggammacs[i] + loggammars[i]) for i in cmps]