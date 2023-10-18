def Lindsay_Bromley(T, ys, ks, mus, Tbs, MWs):
    r'''Calculates thermal conductivity of a gas mixture according to
    mixing rules in [1]_ and also in [2]_.

    .. math::
        k = \sum \frac{y_i k_i}{\sum y_i A_{ij}}

        A_{ij} = \frac{1}{4} \left\{ 1 + \left[\frac{\eta_i}{\eta_j}
        \left(\frac{MW_j}{MW_i}\right)^{0.75} \left( \frac{T+S_i}{T+S_j}\right)
        \right]^{0.5} \right\}^2 \left( \frac{T+S_{ij}}{T+S_i}\right)

        S_{ij} = S_{ji} = (S_i S_j)^{0.5}

    Parameters
    ----------
    T : float
        Temperature of gas [K]
    ys : float
        Mole fractions of gas components
    ks : float
        Liquid thermal conductivites of all components, [W/m/K]
    mus : float
        Gas viscosities of all components, [Pa*S]
    Tbs : float
        Boiling points of all components, [K]
    MWs : float
        Molecular weights of all components, [g/mol]

    Returns
    -------
    kg : float
        Thermal conductivity of gas mixture, [W/m/K]

    Notes
    -----
    This equation is entirely dimensionless; all dimensions cancel.
    The example is from [2]_; all results agree.
    The original source has not been reviewed.

    DIPPR Procedure 9D: Method for the Thermal Conductivity of Gas Mixtures

    Average deviations of 4-5% for 77 binary mixtures reviewed in [2]_, from
    1342 points; also six ternary mixtures (70  points); max deviation observed
    was 40%. (DIPPR)

    TODO: Finish documenting this.

    Examples
    --------
    >>> Lindsay_Bromley(323.15, [0.23, 0.77], [1.939E-2, 1.231E-2], [1.002E-5, 1.015E-5], [248.31, 248.93], [46.07, 50.49])
    0.01390264417969313

    References
    ----------
    .. [1] Lindsay, Alexander L., and LeRoy A. Bromley. "Thermal Conductivity
       of Gas Mixtures." Industrial & Engineering Chemistry 42, no. 8
       (August 1, 1950): 1508-11. doi:10.1021/ie50488a017.
    .. [2] Danner, Ronald P, and Design Institute for Physical Property Data.
       Manual for Predicting Chemical Process Design Data. New York, N.Y, 1982.
    '''
    if not none_and_length_check([ys, ks, mus, Tbs, MWs]):
        raise Exception('Function inputs are incorrect format')

    cmps = range(len(ys))
    Ss = [1.5*Tb for Tb in Tbs]
    Sij = [[(Si*Sj)**0.5 for Sj in Ss] for Si in Ss]

    Aij = [[0.25*(1. + (mus[i]/mus[j]*(MWs[j]/MWs[i])**0.75
            *(T+Ss[i])/(T+Ss[j]))**0.5 )**2 *(T+Sij[i][j])/(T+Ss[i])
            for j in cmps] for i in cmps]
            
    return sum([ys[i]*ks[i]/sum(ys[j]*Aij[i][j] for j in cmps) for i in cmps])