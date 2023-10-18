def Lastovka_solid(T, similarity_variable):
    r'''Calculate solid constant-pressure heat capacitiy with the similarity
    variable concept and method as shown in [1]_.

    .. math::
        C_p = 3(A_1\alpha + A_2\alpha^2)R\left(\frac{\theta}{T}\right)^2
        \frac{\exp(\theta/T)}{[\exp(\theta/T)-1]^2}
        + (C_1\alpha + C_2\alpha^2)T + (D_1\alpha + D_2\alpha^2)T^2

    Parameters
    ----------
    T : float
        Temperature of solid [K]
    similarity_variable : float
        similarity variable as defined in [1]_, [mol/g]

    Returns
    -------
    Cps : float
        Solid constant-pressure heat capacitiy, [J/kg/K]

    Notes
    -----
    Many restrictions on its use. Trained on data with MW from 12.24 g/mol
    to 402.4 g/mol, C mass fractions from 61.3% to 95.2%,
    H mass fractions from 3.73% to 15.2%, N mass fractions from 0 to 15.4%,
    O mass fractions from 0 to 18.8%, and S mass fractions from 0 to 29.6%.
    Recommended for organic compounds with low mass fractions of hetero-atoms
    and especially when molar mass exceeds 200 g/mol. This model does not show
    and effects of phase transition but should not be used passed the triple
    point.

    Original model is in terms of J/g/K. Note that the model s for predicting
    mass heat capacity, not molar heat capacity like most other methods!

    A1 = 0.013183; A2 = 0.249381; theta = 151.8675; C1 = 0.026526;
    C2 = -0.024942; D1 = 0.000025; D2 = -0.000123.

    Examples
    --------
    >>> Lastovka_solid(300, 0.2139)
    1682.063629222013

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

    Cp = (3*(A1*similarity_variable + A2*similarity_variable**2)*R*(theta/T
    )**2*exp(theta/T)/(exp(theta/T)-1)**2
    + (C1*similarity_variable + C2*similarity_variable**2)*T
    + (D1*similarity_variable + D2*similarity_variable**2)*T**2)
    Cp = Cp*1000 # J/g/K to J/kg/K
    return Cp