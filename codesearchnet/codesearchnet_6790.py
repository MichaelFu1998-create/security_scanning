def Velasco(T, Tc, omega):
    r'''Calculates enthalpy of vaporization at arbitrary temperatures using a
    the work of [1]_; requires a chemical's critical temperature and
    acentric factor.

    The enthalpy of vaporization is given by:

    .. math::
        \Delta_{vap} H = RT_c(7.2729 + 10.4962\omega + 0.6061\omega^2)(1-T_r)^{0.38}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    omega : float
        Acentric factor [-]

    Returns
    -------
    Hvap : float
        Enthalpy of vaporization, [J/mol]

    Notes
    -----
    The original article has been reviewed. It is regressed from enthalpy of
    vaporization values at 0.7Tr, from 121 fluids in REFPROP 9.1.
    A value in the article was read to be similar, but slightly too low from
    that calculated here.

    Examples
    --------
    From graph, in [1]_ for perfluoro-n-heptane.

    >>> Velasco(333.2, 476.0, 0.5559)
    33299.41734936356

    References
    ----------
    .. [1] Velasco, S., M. J. Santos, and J. A. White. "Extended Corresponding
       States Expressions for the Changes in Enthalpy, Compressibility Factor
       and Constant-Volume Heat Capacity at Vaporization." The Journal of
       Chemical Thermodynamics 85 (June 2015): 68-76.
       doi:10.1016/j.jct.2015.01.011.
    '''
    return (7.2729 + 10.4962*omega + 0.6061*omega**2)*(1-T/Tc)**0.38*R*Tc