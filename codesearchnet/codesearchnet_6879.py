def Miqueu(T, Tc, Vc, omega):
    r'''Calculates air-water surface tension using the methods of [1]_.

    .. math::
        \sigma = k T_c \left( \frac{N_a}{V_c}\right)^{2/3}
        (4.35 + 4.14 \omega)t^{1.26}(1+0.19t^{0.5} - 0.487t)

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Vc : float
        Critical volume of fluid [m^3/mol]
    omega : float
        Acentric factor for fluid, [-]

    Returns
    -------
    sigma : float
        Liquid surface tension, N/m

    Notes
    -----
    Uses Avogadro's constant and the Boltsman constant.
    Internal units of volume are mL/mol and mN/m. However, either a typo
    is in the article or author's work, or my value of k is off by 10; this is
    corrected nonetheless.
    Created with 31 normal fluids, none polar or hydrogen bonded. Has an
    AARD of 3.5%.

    Examples
    --------
    Bromotrifluoromethane, 2.45 mN/m

    >>> Miqueu(300., 340.1, 0.000199, 0.1687)
    0.003474099603581931

    References
    ----------
    .. [1] Miqueu, C, D Broseta, J Satherley, B Mendiboure, J Lachaise, and
       A Graciaa. "An Extended Scaled Equation for the Temperature Dependence
       of the Surface Tension of Pure Compounds Inferred from an Analysis of
       Experimental Data." Fluid Phase Equilibria 172, no. 2 (July 5, 2000):
       169-82. doi:10.1016/S0378-3812(00)00384-8.
    '''
    Vc = Vc*1E6
    t = 1.-T/Tc
    sigma = k*Tc*(N_A/Vc)**(2/3.)*(4.35 + 4.14*omega)*t**1.26*(1+0.19*t**0.5 - 0.25*t)*10000
    return sigma