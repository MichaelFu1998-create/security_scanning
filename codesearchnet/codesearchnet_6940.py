def Stiel_Thodos(T, Tc, Pc, MW):
    r'''Calculates the viscosity of a gas using an emperical formula
    developed in [1]_.

    .. math::
        TODO

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
    Untested.
    Claimed applicability from 0.2 to 5 atm.
    Developed with data from 52 nonpolar, and 53 polar gases.
    internal units are poise and atm.
    Seems to give reasonable results.

    Examples
    --------
    >>> Stiel_Thodos(300., 556.35, 4.5596E6, 153.8) #CCl4
    1.0408926223608723e-05

    References
    ----------
    .. [1] Stiel, Leonard I., and George Thodos. "The Viscosity of Nonpolar
       Gases at Normal Pressures." AIChE Journal 7, no. 4 (1961): 611-15.
       doi:10.1002/aic.690070416.
    '''
    Pc = Pc/101325.
    Tr = T/Tc
    xi = Tc**(1/6.)/(MW**0.5*Pc**(2/3.))
    if Tr > 1.5:
        mu_g = 17.78E-5*(4.58*Tr-1.67)**.625/xi
    else:
        mu_g = 34E-5*Tr**0.94/xi
    return mu_g/1000.