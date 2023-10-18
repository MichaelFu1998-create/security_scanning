def Lastovka_Shaw_integral_over_T(T, similarity_variable, cyclic_aliphatic=False):
    r'''Calculate the integral over temperature of ideal-gas constant-pressure 
    heat capacitiy with the similarity variable concept and method as shown in
    [1]_.

    Parameters
    ----------
    T : float
        Temperature of gas [K]
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
    Integral was computed with SymPy.

    See Also
    --------
    Lastovka_Shaw
    Lastovka_Shaw_integral

    Examples
    --------
    >>> Lastovka_Shaw_integral_over_T(300.0, 0.1333)
    3609.791928945323

    References
    ----------
    .. [1] Lastovka, Vaclav, and John M. Shaw. "Predictive Correlations for
       Ideal Gas Heat Capacities of Pure Hydrocarbons and Petroleum Fractions."
       Fluid Phase Equilibria 356 (October 25, 2013): 338-370.
       doi:10.1016/j.fluid.2013.07.023.
    '''
    from cmath import log, exp
    a = similarity_variable
    if cyclic_aliphatic:
        A1 = -0.1793547
        A2 = 3.86944439
        first = A1 + A2*a
    else:
        A1 = 0.58
        A2 = 1.25
        A3 = 0.17338003 # 803 instead of 8003 in another paper
        A4 = 0.014
        first = A2 + (A1-A2)/(1. + exp((a - A3)/A4))

    a2 = a*a
    B11 = 0.73917383
    B12 = 8.88308889
    C11 = 1188.28051
    C12 = 1813.04613
    B21 = 0.0483019
    B22 = 4.35656721
    C21 = 2897.01927
    C22 = 5987.80407
    S = (first*log(T) + (-B11 - B12*a)*log(exp((-C11 - C12*a)/T) - 1.) 
        + (-B11*C11 - B11*C12*a - B12*C11*a - B12*C12*a2)/(T*exp((-C11
        - C12*a)/T) - T) - (B11*C11 + B11*C12*a + B12*C11*a + B12*C12*a2)/T)
    S += ((-B21 - B22*a)*log(exp((-C21 - C22*a)/T) - 1.) + (-B21*C21 - B21*C22*a
        - B22*C21*a - B22*C22*a2)/(T*exp((-C21 - C22*a)/T) - T) - (B21*C21
        + B21*C22*a + B22*C21*a + B22*C22*a**2)/T)
    # There is a non-real component, but it is only a function of similariy 
    # variable and so will always cancel out.
    return S.real*1000.