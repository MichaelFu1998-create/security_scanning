def Mersmann_Kind_thermal_conductivity_liquid(T, MW, Tc, Vc, atoms):
    r'''Estimates the thermal conductivity of organic liquid substances
    according to the method of [1]_.

    .. math::
        \lambda^* = \frac{\lambda\cdot V_c^{2/3}\cdot T_c\cdot \text{MW}^{0.5}}
        {(k\cdot T_c)^{1.5}\cdot N_A^{7/6}}

        \lambda^* = \frac{2}{3}\left(n_a + 40\sqrt{1-T_r}\right)
        
    Parameters
    ----------
    T : float
        Temperature of the fluid [K]
    M : float
        Molecular weight of the fluid [g/mol]
    Tc : float
        Critical temperature of the fluid [K]
    Vc : float
        Critical volume of the fluid [m^3/mol]
    atoms : dict
        Dictionary of atoms and their counts, [-]

    Returns
    -------
    kl : float
        Estimated liquid thermal conductivity [W/m/k]

    Notes
    -----
    In the equation, all quantities must be in SI units but N_A is in a kmol
    basis and Vc is in units of (m^3/kmol); this is converted internally.
    
    Examples
    --------
    Dodecane at 400 K:
        
    >>> Mersmann_Kind_thermal_conductivity_liquid(400, 170.33484, 658.0, 
    ... 0.000754, {'C': 12, 'H': 26})
    0.08952713798442789

    References
    ----------
    .. [1] Mersmann, Alfons, and Matthias Kind. "Prediction of Mechanical and 
       Thermal Properties of Pure Liquids, of Critical Data, and of Vapor 
       Pressure." Industrial & Engineering Chemistry Research, January 31, 
       2017. https://doi.org/10.1021/acs.iecr.6b04323.
    '''
    na = sum(atoms.values())
    lambda_star = 2/3.*(na + 40.*(1. - T/Tc)**0.5)
    Vc = Vc*1000 # m^3/mol to m^3/kmol
    N_A2 = N_A*1000 # Their avogadro's constant is per kmol
    kl = lambda_star*(k*Tc)**1.5*N_A2**(7/6.)*Vc**(-2/3.)/Tc*MW**-0.5
    return kl