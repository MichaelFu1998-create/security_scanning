def Clapeyron(T, Tc, Pc, dZ=1, Psat=101325):
    r'''Calculates enthalpy of vaporization at arbitrary temperatures using the
    Clapeyron equation.

    The enthalpy of vaporization is given by:

    .. math::
        \Delta H_{vap} = RT \Delta Z \frac{\ln (P_c/Psat)}{(1-T_{r})}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]
    dZ : float
        Change in compressibility factor between liquid and gas, []
    Psat : float
        Saturation pressure of fluid [Pa], optional

    Returns
    -------
    Hvap : float
        Enthalpy of vaporization, [J/mol]

    Notes
    -----
    No original source is available for this equation.
    [1]_ claims this equation overpredicts enthalpy by several percent.
    Under Tr = 0.8, dZ = 1 is a reasonable assumption.
    This equation is most accurate at the normal boiling point.

    Internal units are bar.

    WARNING: I believe it possible that the adjustment for pressure may be incorrect

    Examples
    --------
    Problem from Perry's examples.

    >>> Clapeyron(T=294.0, Tc=466.0, Pc=5.55E6)
    26512.354585061985

    References
    ----------
    .. [1] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
       New York: McGraw-Hill Professional, 2000.
    '''
    Tr = T/Tc
    return R*T*dZ*log(Pc/Psat)/(1. - Tr)