def Aleem(T, MW, Tb, rhol, Hvap_Tb, Cpl):
    r'''Calculates vapor-liquid surface tension using the correlation derived by
    [1]_ based on critical property CSP methods.

    .. math::
        \sigma = \phi \frac{MW^{1/3}} {6N_A^{1/3}}\rho_l^{2/3}\left[H_{vap}
        + C_{p,l}(T_b-T)\right]

        \phi = 1 - 0.0047MW + 6.8\times 10^{-6} MW^2
            
    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    MW : float
        Molecular weight [g/mol]
    Tb : float
        Boiling temperature of the fluid [K]
    rhol : float
        Liquid density at T and P [kg/m^3]
    Hvap_Tb : float
        Mass enthalpy of vaporization at the normal boiling point [kg/m^3]
    Cpl : float
        Liquid heat capacity of the chemical at T [J/kg/K]

    Returns
    -------
    sigma : float
        Liquid-vapor surface tension [N/m]

    Notes
    -----
    Internal units of molecuar weight are kg/mol. This model is dimensionally
    consistent.
    
    This model does not use the critical temperature. After it predicts a 
    surface tension of 0 at a sufficiently high temperature, it returns 
    negative results. The temperature at which this occurs (the "predicted"
    critical temperature) can be calculated as follows:
        
    .. math::
        \sigma = 0 \to T_{c,predicted} \text{ at } T_b + \frac{H_{vap}}{Cp_l}
    
    Because of its dependence on density, it has the potential to model the 
    effect of pressure on surface tension.
    
    Claims AAD of 4.3%. Developed for normal alkanes. Total of 472 data points. 
    Behaves worse for higher alkanes. Behaves very poorly overall.
    
    Examples
    --------
    Methane at 90 K
    
    >>> Aleem(T=90, MW=16.04246, Tb=111.6, rhol=458.7, Hvap_Tb=510870.,
    ... Cpl=2465.)
    0.01669970221165325

    References
    ----------
    .. [1] Aleem, W., N. Mellon, S. Sufian, M. I. A. Mutalib, and D. Subbarao.
       "A Model for the Estimation of Surface Tension of Pure Hydrocarbon 
       Liquids." Petroleum Science and Technology 33, no. 23-24 (December 17, 
       2015): 1908-15. doi:10.1080/10916466.2015.1110593.
    '''
    MW = MW/1000. # Use kg/mol for consistency with the other units
    sphericity = 1. - 0.0047*MW + 6.8E-6*MW*MW
    return sphericity*MW**(1/3.)/(6.*N_A**(1/3.))*rhol**(2/3.)*(Hvap_Tb + Cpl*(Tb-T))