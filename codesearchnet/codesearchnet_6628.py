def Dadgostar_Shaw_integral(T, similarity_variable):
    r'''Calculate the integral of liquid constant-pressure heat capacitiy 
    with the similarity variable concept and method as shown in [1]_.

    Parameters
    ----------
    T : float
        Temperature of gas [K]
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
    Integral was computed with SymPy.

    See Also
    --------
    Dadgostar_Shaw
    Dadgostar_Shaw_integral_over_T

    Examples
    --------
    >>> Dadgostar_Shaw_integral(300.0, 0.1333)
    238908.15142664989

    References
    ----------
    .. [1] Dadgostar, Nafiseh, and John M. Shaw. "A Predictive Correlation for
       the Constant-Pressure Specific Heat Capacity of Pure and Ill-Defined
       Liquid Hydrocarbons." Fluid Phase Equilibria 313 (January 15, 2012):
       211-226. doi:10.1016/j.fluid.2011.09.015.
    '''
    a = similarity_variable
    a2 = a*a
    T2 = T*T
    a11 = -0.3416
    a12 = 2.2671
    a21 = 0.1064
    a22 = -0.3874
    a31 = -9.8231E-05
    a32 = 4.182E-04
    constant = 24.5
    H = T2*T/3.*(a2*a32 + a*a31) + T2*0.5*(a2*a22 + a*a21) + T*constant*(a2*a12 + a*a11)
    return H*1000.