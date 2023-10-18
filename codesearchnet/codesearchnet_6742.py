def boiling_critical_relation(T, Tb, Tc, Pc):
    r'''Calculates vapor pressure of a fluid at arbitrary temperatures using a
    CSP relationship as in [1]_; requires a chemical's critical temperature
    and pressure as well as boiling point.

    The vapor pressure is given by:

    .. math::
        \ln P^{sat}_r = h\left( 1 - \frac{1}{T_r}\right)

        h = T_{br} \frac{\ln(P_c/101325)}{1-T_{br}}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tb : float
        Boiling temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]

    Returns
    -------
    Psat : float
        Vapor pressure at T [Pa]

    Notes
    -----
    Units are Pa. Formulation makes intuitive sense; a logarithmic form of
    interpolation.

    Examples
    --------
    Example as in [1]_ for ethylbenzene

    >>> boiling_critical_relation(347.2, 409.3, 617.1, 36E5)
    15209.467273093938

    References
    ----------
    .. [1] Reid, Robert C..; Prausnitz, John M.;; Poling, Bruce E.
       The Properties of Gases and Liquids. McGraw-Hill Companies, 1987.
    '''
    Tbr = Tb/Tc
    Tr = T/Tc
    h = Tbr*log(Pc/101325.)/(1 - Tbr)
    return exp(h*(1-1/Tr))*Pc