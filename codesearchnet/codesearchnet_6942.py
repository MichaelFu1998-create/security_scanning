def Gharagheizi_gas_viscosity(T, Tc, Pc, MW):
    r'''Calculates the viscosity of a gas using an emperical formula
    developed in [1]_.

    .. math::
        \mu = 10^{-7} | 10^{-5} P_cT_r + \left(0.091-\frac{0.477}{M}\right)T +
        M \left(10^{-5}P_c-\frac{8M^2}{T^2}\right)
        \left(\frac{10.7639}{T_c}-\frac{4.1929}{T}\right)|

    Parameters
    ----------
    T : float
        Temperature of the fluid [K]
    Tc : float
        Critical temperature of the fluid [K]
    Pc : float
        Critical pressure of the fluid [Pa]
    MW : float
        Molwcular weight of fluid [g/mol]

    Returns
    -------
    mu_g : float
        Viscosity of gas, [Pa*S]

    Notes
    -----
    Example is first point in supporting information of article, for methane.
    This is the prefered function for gas viscosity.
    7% average relative deviation. Deviation should never be above 30%.
    Developed with the DIPPR database. It is believed theoretically predicted values
    are included in the correlation.

    Examples
    --------
    >>> Gharagheizi_gas_viscosity(120., 190.564, 45.99E5, 16.04246)
    5.215761625399613e-06

    References
    ----------
    .. [1] Gharagheizi, Farhad, Ali Eslamimanesh, Mehdi Sattari, Amir H.
       Mohammadi, and Dominique Richon. "Corresponding States Method for
       Determination of the Viscosity of Gases at Atmospheric Pressure."
       Industrial & Engineering Chemistry Research 51, no. 7
       (February 22, 2012): 3179-85. doi:10.1021/ie202591f.
    '''
    Tr = T/Tc
    mu_g = 1E-5*Pc*Tr + (0.091 - 0.477/MW)*T + MW*(1E-5*Pc - 8*MW**2/T**2)*(10.7639/Tc - 4.1929/T)
    return 1E-7 * abs(mu_g)