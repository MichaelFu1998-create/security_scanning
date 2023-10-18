def Yoon_Thodos(T, Tc, Pc, MW):
    r'''Calculates the viscosity of a gas using an emperical formula
    developed in [1]_.

    .. math::
        \eta \xi \times 10^8 = 46.10 T_r^{0.618} - 20.40 \exp(-0.449T_r) + 1
        9.40\exp(-4.058T_r)+1

        \xi = 2173.424 T_c^{1/6} MW^{-1/2} P_c^{-2/3}

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
    This equation has been tested. The equation uses SI units only internally.
    The constant 2173.424 is an adjustment factor for units.
    Average deviation within 3% for most compounds.
    Greatest accuracy with dipole moments close to 0.
    Hydrogen and helium have different coefficients, not implemented.
    This is DIPPR Procedure 8B: Method for the Viscosity of Pure,
    non hydrocarbon, nonpolar gases at low pressures

    Examples
    --------
    >>> Yoon_Thodos(300., 556.35, 4.5596E6, 153.8)
    1.0194885727776819e-05

    References
    ----------
    .. [1]  Yoon, Poong, and George Thodos. "Viscosity of Nonpolar Gaseous
       Mixtures at Normal Pressures." AIChE Journal 16, no. 2 (1970): 300-304.
       doi:10.1002/aic.690160225.
    '''
    Tr = T/Tc
    xi = 2173.4241*Tc**(1/6.)/(MW**0.5*Pc**(2/3.))
    a = 46.1
    b = 0.618
    c = 20.4
    d = -0.449
    e = 19.4
    f = -4.058
    return (1. + a*Tr**b - c * exp(d*Tr) + e*exp(f*Tr))/(1E8*xi)