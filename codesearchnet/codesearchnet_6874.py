def Brock_Bird(T, Tb, Tc, Pc):
    r'''Calculates air-water surface tension  using the [1]_
    emperical method. Old and tested.

    .. math::
        \sigma = P_c^{2/3}T_c^{1/3}Q(1-T_r)^{11/9}

        Q = 0.1196 \left[ 1 + \frac{T_{br}\ln (P_c/1.01325)}{1-T_{br}}\right]-0.279

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tb : float
        Boiling temperature of the fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]

    Returns
    -------
    sigma : float
        Liquid surface tension, N/m

    Notes
    -----
    Numerous arrangements of this equation are available.
    This is DIPPR Procedure 7A: Method for the Surface Tension of Pure,
    Nonpolar, Nonhydrocarbon Liquids
    The exact equation is not in the original paper.
    If the equation yields a negative result, return None.

    Examples
    --------
    p-dichloribenzene at 412.15 K, from DIPPR; value differs due to a slight
    difference in method.

    >>> Brock_Bird(412.15, 447.3, 685, 3.952E6)
    0.02208448325192495

    Chlorobenzene from Poling, as compared with a % error value at 293 K.

    >>> Brock_Bird(293.15, 404.75, 633.0, 4530000.0)
    0.032985686413713036

    References
    ----------
    .. [1] Brock, James R., and R. Byron Bird. "Surface Tension and the
       Principle of Corresponding States." AIChE Journal 1, no. 2
       (June 1, 1955): 174-77. doi:10.1002/aic.690010208
    '''
    Tbr = Tb/Tc
    Tr = T/Tc
    Pc = Pc/1E5  # Convert to bar
    Q = 0.1196*(1 + Tbr*log(Pc/1.01325)/(1-Tbr))-0.279
    sigma = (Pc)**(2/3.)*Tc**(1/3.)*Q*(1-Tr)**(11/9.)
    sigma = sigma/1000  # convert to N/m
    return sigma