def Tstar(T, epsilon_k=None, epsilon=None):
    r'''This function calculates the parameter `Tstar` as needed in performing
    collision integral calculations.

    .. math::
        T^* = \frac{kT}{\epsilon}

    Examples
    --------
    >>> Tstar(T=318.2, epsilon_k=308.43)
    1.0316765554582887

    Parameters
    ----------
    epsilon_k : float, optional
        Lennard-Jones depth of potential-energy minimum over k, [K]
    epsilon : float, optional
        Lennard-Jones depth of potential-energy minimum [J]

    Returns
    -------
    Tstar : float
        Dimentionless temperature for calculating collision integral, [-]

    Notes
    -----
    Tabulated values are normally listed as epsilon/k. k is the Boltzman
    constant, with units of J/K.

    References
    ----------
    .. [1] Bird, R. Byron, Warren E. Stewart, and Edwin N. Lightfoot.
       Transport Phenomena, Revised 2nd Edition. New York:
       John Wiley & Sons, Inc., 2006
    '''
    if epsilon_k:
        _Tstar = T/(epsilon_k)
    elif epsilon:
        _Tstar = k*T/epsilon
    else:
        raise Exception('Either epsilon/k or epsilon must be provided')
    return _Tstar