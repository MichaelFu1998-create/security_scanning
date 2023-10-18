def Sastri_Rao(T, Tb, Tc, Pc, chemicaltype=None):
    r'''Calculates air-water surface tension using the correlation derived by
    [1]_ based on critical property CSP methods and chemical classes.

    .. math::
        \sigma = K P_c^xT_b^y T_c^z\left[\frac{1-T_r}{1-T_{br}}\right]^m

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tb : float
        Boiling temperature of the fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]

    Returns
    -------
    sigma : float
        Liquid surface tension, N/m

    Notes
    -----
    The source of this equation has not been reviewed.
    Internal units of presure are bar, surface tension of mN/m.

    Examples
    --------
    Chlorobenzene from Poling, as compared with a % error value at 293 K.

    >>> Sastri_Rao(293.15, 404.75, 633.0, 4530000.0)
    0.03234567739694441

    References
    ----------
    .. [1] Sastri, S. R. S., and K. K. Rao. "A Simple Method to Predict
       Surface Tension of Organic Liquids." The Chemical Engineering Journal
       and the Biochemical Engineering Journal 59, no. 2 (October 1995): 181-86.
       doi:10.1016/0923-0467(94)02946-6.
    '''
    if chemicaltype == 'alcohol':
        k, x, y, z, m = 2.28, 0.25, 0.175, 0, 0.8
    elif chemicaltype == 'acid':
        k, x, y, z, m = 0.125, 0.50, -1.5, 1.85, 11/9.0
    else:
        k, x, y, z, m = 0.158, 0.50, -1.5, 1.85, 11/9.0
    Tr = T/Tc
    Tbr = Tb/Tc
    Pc = Pc/1E5  # Convert to bar
    sigma = k*Pc**x*Tb**y*Tc**z*((1 - Tr)/(1 - Tbr))**m
    sigma = sigma/1000  # N/m
    return sigma