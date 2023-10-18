def Lastovka_solid_integral(T, similarity_variable):
    r'''Integrates solid constant-pressure heat capacitiy with the similarity
    variable concept and method as shown in [1]_.
    
    Uses a explicit form as derived with Sympy.

    Parameters
    ----------
    T : float
        Temperature of solid [K]
    similarity_variable : float
        similarity variable as defined in [1]_, [mol/g]

    Returns
    -------
    H : float
        Difference in enthalpy from 0 K, [J/kg]

    Notes
    -----
    Original model is in terms of J/g/K. Note that the model is for predicting
    mass heat capacity, not molar heat capacity like most other methods!

    See Also
    --------
    Lastovka_solid

    Examples
    --------
    >>> Lastovka_solid_integral(300, 0.2139)
    283246.1242170376

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
    similarity_variable2 = similarity_variable*similarity_variable
    
    return (T*T*T*(1000.*D1*similarity_variable/3. 
        + 1000.*D2*similarity_variable2/3.) + T*T*(500.*C1*similarity_variable 
        + 500.*C2*similarity_variable2)
        + (3000.*A1*R*similarity_variable*theta
        + 3000.*A2*R*similarity_variable2*theta)/(exp(theta/T) - 1.))