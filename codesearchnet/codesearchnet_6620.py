def Lastovka_Shaw(T, similarity_variable, cyclic_aliphatic=False):
    r'''Calculate ideal-gas constant-pressure heat capacitiy with the similarity
    variable concept and method as shown in [1]_.

    .. math::
        C_p^0 = \left(A_2 + \frac{A_1 - A_2}{1 + \exp(\frac{\alpha-A_3}{A_4})}\right)
        + (B_{11} + B_{12}\alpha)\left(-\frac{(C_{11} + C_{12}\alpha)}{T}\right)^2
        \frac{\exp(-(C_{11} + C_{12}\alpha)/T)}{[1-\exp(-(C_{11}+C_{12}\alpha)/T)]^2}\\
        + (B_{21} + B_{22}\alpha)\left(-\frac{(C_{21} + C_{22}\alpha)}{T}\right)^2
        \frac{\exp(-(C_{21} + C_{22}\alpha)/T)}{[1-\exp(-(C_{21}+C_{22}\alpha)/T)]^2}

    Parameters
    ----------
    T : float
        Temperature of gas [K]
    similarity_variable : float
        similarity variable as defined in [1]_, [mol/g]

    Returns
    -------
    Cpg : float
        Gas constant-pressure heat capacitiy, [J/kg/K]

    Notes
    -----
    Original model is in terms of J/g/K. Note that the model is for predicting
    mass heat capacity, not molar heat capacity like most other methods!

    A1 = 0.58, A2 = 1.25, A3 = 0.17338003, A4 = 0.014, B11 = 0.73917383,
    B12 = 8.88308889, C11 = 1188.28051, C12 = 1813.04613, B21 = 0.0483019,
    B22 = 4.35656721, C21 = 2897.01927, C22 = 5987.80407.

    Examples
    --------
    >>> Lastovka_Shaw(1000.0, 0.1333)
    2467.113309084757

    References
    ----------
    .. [1] Lastovka, Vaclav, and John M. Shaw. "Predictive Correlations for
       Ideal Gas Heat Capacities of Pure Hydrocarbons and Petroleum Fractions."
       Fluid Phase Equilibria 356 (October 25, 2013): 338-370.
       doi:10.1016/j.fluid.2013.07.023.
    '''
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
        # Personal communication confirms the change

    B11 = 0.73917383
    B12 = 8.88308889
    C11 = 1188.28051
    C12 = 1813.04613
    B21 = 0.0483019
    B22 = 4.35656721
    C21 = 2897.01927
    C22 = 5987.80407
    Cp = first + (B11 + B12*a)*((C11+C12*a)/T)**2*exp(-(C11 + C12*a)/T)/(1.-exp(-(C11+C12*a)/T))**2
    Cp += (B21 + B22*a)*((C21+C22*a)/T)**2*exp(-(C21 + C22*a)/T)/(1.-exp(-(C21+C22*a)/T))**2
    return Cp*1000.