def Riedel(Tb, Tc, Pc):
    r'''Calculates enthalpy of vaporization at the boiling point, using the
    Ridel [1]_ CSP method. Required information are critical temperature
    and pressure, and boiling point. Equation taken from [2]_ and [3]_.

    The enthalpy of vaporization is given by:

    .. math::
        \Delta_{vap} H=1.093 T_b R\frac{\ln P_c-1.013}{0.930-T_{br}}

    Parameters
    ----------
    Tb : float
        Boiling temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]

    Returns
    -------
    Hvap : float
        Enthalpy of vaporization at the normal boiling point, [J/mol]

    Notes
    -----
    This equation has no example calculation in any source. The source has not
    been verified. It is equation 4-144 in Perry's. Perry's also claims that
    errors seldom surpass 5%.

    [2]_ is the source of example work here, showing a calculation at 0.0%
    error.

    Internal units of pressure are bar.

    Examples
    --------
    Pyridine, 0.0% err vs. exp: 35090 J/mol; from Poling [2]_.

    >>> Riedel(388.4, 620.0, 56.3E5)
    35089.78989646058

    References
    ----------
    .. [1] Riedel, L. "Eine Neue Universelle Dampfdruckformel Untersuchungen
       Uber Eine Erweiterung Des Theorems Der Ubereinstimmenden Zustande. Teil
       I." Chemie Ingenieur Technik 26, no. 2 (February 1, 1954): 83-89.
       doi:10.1002/cite.330260206.
    .. [2] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
       New York: McGraw-Hill Professional, 2000.
    .. [3] Green, Don, and Robert Perry. Perry's Chemical Engineers' Handbook,
       Eighth Edition. McGraw-Hill Professional, 2007.
    '''
    Pc = Pc/1E5  # Pa to bar
    Tbr = Tb/Tc
    return 1.093*Tb*R*(log(Pc) - 1.013)/(0.93 - Tbr)