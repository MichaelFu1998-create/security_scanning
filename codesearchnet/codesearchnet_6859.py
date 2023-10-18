def conductivity_McCleskey(T, M, lambda_coeffs, A_coeffs, B, multiplier, rho=1000.):
    r'''This function handles the calculation of the electrical conductivity of 
    an electrolytic aqueous solution with one electrolyte in solution. It
    handles temperature dependency and concentrated solutions. Requires the 
    temperature of the solution; its molality, and four sets of coefficients
    `lambda_coeffs`, `A_coeffs`, `B`, and `multiplier`.
    
    .. math::
        \Lambda = \frac{\kappa}{C}
        
        \Lambda = \Lambda^0(t) - A(t) \frac{m^{1/2}}{1+Bm^{1/2}}
        
        \Lambda^\circ(t) = c_1 t^2 + c_2 t + c_3
        
        A(t) = d_1 t^2 + d_2 t + d_3
        
    In the above equations, `t` is temperature in degrees Celcius;
    `m` is molality in mol/kg, and C is the concentration of the elctrolytes
    in mol/m^3, calculated as the product of density and molality.
    
    Parameters
    ----------
    T : float
        Temperature of the solution, [K]
    M : float
        Molality of the solution with respect to one electrolyte
        (mol solute / kg solvent), [mol/kg]
    lambda_coeffs : list[float]
        List of coefficients for the polynomial used to calculate `lambda`;
        length-3 coefficients provided in [1]_,  [-]
    A_coeffs : list[float]
        List of coefficients for the polynomial used to calculate `A`;
        length-3 coefficients provided in [1]_, [-]
    B : float
        Empirical constant for an electrolyte, [-]
    multiplier : float
        The multiplier to obtain the absolute conductivity from the equivalent
        conductivity; ex 2 for CaCl2, [-]
    rho : float, optional
        The mass density of the aqueous mixture, [kg/m^3]

    Returns
    -------
    kappa : float
        Electrical conductivity of the solution at the specified molality and 
        temperature [S/m]

    Notes
    -----
    Coefficients provided in [1]_ result in conductivity being calculated in
    units of mS/cm; they are converted to S/m before returned.

    Examples
    --------
    A 0.5 wt% solution of CaCl2, conductivity calculated in mS/cm
    
    >>> conductivity_McCleskey(T=293.15, M=0.045053, A_coeffs=[.03918, 3.905, 
    ... 137.7], lambda_coeffs=[0.01124, 2.224, 72.36], B=3.8, multiplier=2)
    0.8482584585108555

    References
    ----------
    .. [1] McCleskey, R. Blaine. "Electrical Conductivity of Electrolytes Found
       In Natural Waters from (5 to 90) °C." Journal of Chemical & Engineering 
       Data 56, no. 2 (February 10, 2011): 317-27. doi:10.1021/je101012n.
    '''
    t = T - 273.15
    lambda_coeff = horner(lambda_coeffs, t)
    A = horner(A_coeffs, t)
    M_root = M**0.5
    param = lambda_coeff - A*M_root/(1. + B*M_root)
    C = M*rho/1000. # convert to mol/L to get concentration
    return param*C*multiplier*0.1