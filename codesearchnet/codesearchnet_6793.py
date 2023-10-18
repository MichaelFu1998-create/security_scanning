def Liu(Tb, Tc, Pc):
    r'''Calculates enthalpy of vaporization at the normal boiling point using
    the Liu [1]_ correlation, and a chemical's critical temperature, pressure
    and boiling point.

    The enthalpy of vaporization is given by:

    .. math::
        \Delta H_{vap} = RT_b \left[ \frac{T_b}{220}\right]^{0.0627} \frac{
        (1-T_{br})^{0.38} \ln(P_c/P_A)}{1-T_{br} + 0.38 T_{br} \ln T_{br}}

    Parameters
    ----------
    Tb : float
        Boiling temperature of the fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]

    Returns
    -------
    Hvap : float
        Enthalpy of vaporization, [J/mol]

    Notes
    -----
    This formulation can be adjusted for lower boiling points, due to the use
    of a rationalized pressure relationship. The formulation is taken from
    the original article.

    A correction for alcohols and organic acids based on carbon number,
    which only modifies the boiling point, is available but not implemented.

    No sample calculations are available in the article.

    Internal units: Pa and K

    Examples
    --------
    Same problem as in Perry's examples

    >>> Liu(294.0, 466.0, 5.55E6)
    26378.566319606754

    References
    ----------
    .. [1] LIU, ZHI-YONG. "Estimation of Heat of Vaporization of Pure Liquid at
       Its Normal Boiling Temperature." Chemical Engineering Communications
       184, no. 1 (February 1, 2001): 221-28. doi:10.1080/00986440108912849.
    '''
    Tbr = Tb/Tc
    return R*Tb*(Tb/220.)**0.0627*(1. - Tbr)**0.38*log(Pc/101325.) \
        / (1 - Tbr + 0.38*Tbr*log(Tbr))