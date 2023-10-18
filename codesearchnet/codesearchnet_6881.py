def Mersmann_Kind_surface_tension(T, Tm, Tb, Tc, Pc, n_associated=1):
    r'''Estimates the surface tension of organic liquid substances
    according to the method of [1]_.

    .. math::
        \sigma^* = \frac{\sigma n_{ass}^{1/3}} {(kT_c)^{1/3} T_{rm}P_c^{2/3}}
        
        \sigma^* = \left(\frac{T_b - T_m}{T_m}\right)^{1/3}
        \left[6.25(1-T_r) + 31.3(1-T_r)^{4/3}\right]
        
    Parameters
    ----------
    T : float
        Temperature of the fluid [K]
    Tm : float
        Melting temperature [K]
    Tb : float
        Boiling temperature of the fluid [K]
    Tc : float
        Critical temperature of the fluid [K]
    Pc : float
        Critical pressure of the fluid [Pa]
    n_associated : float
        Number of associated molecules in a cluster (2 for alcohols, 1
        otherwise), [-]

    Returns
    -------
    sigma : float
        Liquid-vapor surface tension [N/m]

    Notes
    -----
    In the equation, all quantities must be in SI units. `k` is the boltzman
    constant.
    
    Examples
    --------
    MTBE at STP (the actual value is 0.0181):
        
    >>> Mersmann_Kind_surface_tension(298.15, 164.15, 328.25, 497.1, 3430000.0)
    0.016744309508833335

    References
    ----------
    .. [1] Mersmann, Alfons, and Matthias Kind. "Prediction of Mechanical and 
       Thermal Properties of Pure Liquids, of Critical Data, and of Vapor 
       Pressure." Industrial & Engineering Chemistry Research, January 31, 
       2017. https://doi.org/10.1021/acs.iecr.6b04323.
    '''
    Tr = T/Tc
    sigma_star = ((Tb - Tm)/Tm)**(1/3.)*(6.25*(1. - Tr) + 31.3*(1. - Tr)**(4/3.))
    sigma = sigma_star*(k*Tc)**(1/3.)*(Tm/Tc)*Pc**(2/3.)*n_associated**(-1/3.)
    return sigma