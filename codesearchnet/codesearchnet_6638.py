def Lastovka_solid_integral_over_T(T, similarity_variable):
    r'''Integrates over T solid constant-pressure heat capacitiy with the 
    similarity variable concept and method as shown in [1]_.
    
    Uses a explicit form as derived with Sympy.

    Parameters
    ----------
    T : float
        Temperature of solid [K]
    similarity_variable : float
        similarity variable as defined in [1]_, [mol/g]

    Returns
    -------
    S : float
        Difference in entropy from 0 K, [J/kg/K]

    Notes
    -----
    Original model is in terms of J/g/K. Note that the model is for predicting
    mass heat capacity, not molar heat capacity like most other methods!

    See Also
    --------
    Lastovka_solid

    Examples
    --------
    >>> Lastovka_solid_integral_over_T(300, 0.2139)
    1947.553552666818

    References
    ----------
    .. [1] Laštovka, Václav, Michal Fulem, Mildred Becerra, and John M. Shaw.
       "A Similarity Variable for Estimating the Heat Capacity of Solid Organic
       Compounds: Part II. Application: Heat Capacity Calculation for
       Ill-Defined Organic Solids." Fluid Phase Equilibria 268, no. 1-2
       (June 25, 2008): 134-41. doi:10.1016/j.fluid.2008.03.018.
    '''
    A1 = 0.013183
    A2 = 0.249381
    theta = 151.8675
    C1 = 0.026526
    C2 = -0.024942
    D1 = 0.000025
    D2 = -0.000123
    
    sim2 = similarity_variable*similarity_variable
    exp_theta_T = exp(theta/T)
    
    return (-3000.*R*similarity_variable*(A1 + A2*similarity_variable)*log(exp_theta_T - 1.) 
    + T**2*(500.*D1*similarity_variable + 500.*D2*sim2)
    + T*(1000.*C1*similarity_variable + 1000.*C2*sim2)
    + (3000.*A1*R*similarity_variable*theta 
    + 3000.*A2*R*sim2*theta)/(T*exp_theta_T - T) 
    + (3000.*A1*R*similarity_variable*theta 
    + 3000.*A2*R*sim2*theta)/T)