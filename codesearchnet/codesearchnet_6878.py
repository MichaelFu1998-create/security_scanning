def Hakim_Steinberg_Stiel(T, Tc, Pc, omega, StielPolar=0):
    r'''Calculates air-water surface tension using the reference fluids methods
    of [1]_.

    .. math::
        \sigma = 4.60104\times 10^{-7} P_c^{2/3}T_c^{1/3}Q_p \left(\frac{1-T_r}{0.4}\right)^m

        Q_p = 0.1574+0.359\omega-1.769\chi-13.69\chi^2-0.51\omega^2+1.298\omega\chi

        m = 1.21+0.5385\omega-14.61\chi-32.07\chi^2-1.65\omega^2+22.03\omega\chi

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]
    omega : float
        Acentric factor for fluid, [-]
    StielPolar : float, optional
        Stiel Polar Factor, [-]

    Returns
    -------
    sigma : float
        Liquid surface tension, N/m

    Notes
    -----
    Original equation for m and Q are used. Internal units are atm and mN/m.

    Examples
    --------
    1-butanol, as compared to value in CRC Handbook of 0.02493.

    >>> Hakim_Steinberg_Stiel(298.15, 563.0, 4414000.0, 0.59, StielPolar=-0.07872)
    0.021907902575190447

    References
    ----------
    .. [1] Hakim, D. I., David Steinberg, and L. I. Stiel. "Generalized
       Relationship for the Surface Tension of Polar Fluids." Industrial &
       Engineering Chemistry Fundamentals 10, no. 1 (February 1, 1971): 174-75.
       doi:10.1021/i160037a032.
    '''
    Q = (0.1574 + 0.359*omega - 1.769*StielPolar - 13.69*StielPolar**2
        - 0.510*omega**2 + 1.298*StielPolar*omega)
    m = (1.210 + 0.5385*omega - 14.61*StielPolar - 32.07*StielPolar**2
        - 1.656*omega**2 + 22.03*StielPolar*omega)
    Tr = T/Tc
    Pc = Pc/101325.
    sigma = Pc**(2/3.)*Tc**(1/3.)*Q*((1 - Tr)/0.4)**m
    sigma = sigma/1000.  # convert to N/m
    return sigma