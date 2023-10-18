def Letsou_Stiel(T, MW, Tc, Pc, omega):
    r'''Calculates the viscosity of a liquid using an emperical model
    developed in [1]_. However. the fitting parameters for tabulated values
    in the original article are found in ChemSep.

    .. math::
        \xi = \frac{2173.424 T_c^{1/6}}{\sqrt{MW} P_c^{2/3}}

        \xi^{(0)} = (1.5174 - 2.135T_r + 0.75T_r^2)\cdot 10^{-5}

        \xi^{(1)} = (4.2552 - 7.674 T_r + 3.4 T_r^2)\cdot 10^{-5}

        \mu = (\xi^{(0)} + \omega \xi^{(1)})/\xi

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    MW : float
        Molwcular weight of fluid [g/mol]
    Tc : float
        Critical temperature of the fluid [K]
    Pc : float
        Critical pressure of the fluid [Pa]
    omega : float
        Acentric factor of compound

    Returns
    -------
    mu_l : float
        Viscosity of liquid, [Pa*S]

    Notes
    -----
    The form of this equation is a polynomial fit to tabulated data.
    The fitting was performed by the DIPPR. This is DIPPR Procedure 8G: Method
    for the viscosity of pure, nonhydrocarbon liquids at high temperatures
    internal units are SI standard. [1]_'s units were different.
    DIPPR test value for ethanol is used.

    Average error 34%. Range of applicability is 0.76 < Tr < 0.98.

    Examples
    --------
    >>> Letsou_Stiel(400., 46.07, 516.25, 6.383E6, 0.6371)
    0.0002036150875308151

    References
    ----------
    .. [1] Letsou, Athena, and Leonard I. Stiel. "Viscosity of Saturated
       Nonpolar Liquids at Elevated Pressures." AIChE Journal 19, no. 2 (1973):
       409-11. doi:10.1002/aic.690190241.
    '''
    Tr = T/Tc
    xi0 = (1.5174-2.135*Tr + 0.75*Tr**2)*1E-5
    xi1 = (4.2552-7.674*Tr + 3.4*Tr**2)*1E-5
    xi = 2173.424*Tc**(1/6.)/(MW**0.5*Pc**(2/3.))
    return (xi0 + omega*xi1)/xi