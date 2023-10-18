def Kweq_1981(T, rho_w):
    r'''Calculates equilibrium constant for OH- and H+ in water, according to
    [1]_. Second most recent formulation.

    .. math::
        \log_{10} K_w= A + B/T + C/T^2 + D/T^3 + (E+F/T+G/T^2)\log_{10} \rho_w

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    rho_w : float
        Density of water, [kg/m^3]

    Returns
    -------
    Kweq : float
        Ionization constant of water, [-]

    Notes
    -----
    Density is internally converted to units of g/cm^3.

    A = -4.098;
    B = -3245.2;
    C = 2.2362E5;
    D = -3.984E7;
    E = 13.957;
    F = -1262.3;
    G = 8.5641E5

    Examples
    --------
    >>> -1*log10(Kweq_1981(600, 700))
    11.274522047458206
    
    References
    ----------
    .. [1] Marshall, William L., and E. U. Franck. "Ion Product of Water
       Substance, 0-1000  degree C, 1010,000 Bars New International Formulation
       and Its Background." Journal of Physical and Chemical Reference Data 10,
       no. 2 (April 1, 1981): 295-304. doi:10.1063/1.555643.
    '''
    rho_w = rho_w/1000.
    A = -4.098
    B = -3245.2
    C = 2.2362E5
    D = -3.984E7
    E = 13.957
    F = -1262.3
    G = 8.5641E5
    return 10**(A + B/T + C/T**2 + D/T**3 + (E + F/T + G/T**2)*log10(rho_w))