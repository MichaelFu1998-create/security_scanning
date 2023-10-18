def Sato_Riedel(T, M, Tb, Tc):
    r'''Calculate the thermal conductivity of a liquid as a function of
    temperature using the CSP method of Sato-Riedel [1]_, [2]_, published in
    Reid [3]_. Requires temperature, molecular weight, and boiling and critical
    temperatures.

    .. math::
        k = \frac{1.1053}{\sqrt{MW}}\frac{3+20(1-T_r)^{2/3}}
        {3+20(1-T_{br})^{2/3}}

    Parameters
    ----------
    T : float
        Temperature of the fluid [K]
    M : float
        Molecular weight of the fluid [g/mol]
    Tb : float
        Boiling temperature of the fluid [K]
    Tc : float
        Critical temperature of the fluid [K]

    Returns
    -------
    kl : float
        Estimated liquid thermal conductivity [W/m/k]

    Notes
    -----
    This equation has a complicated history. It is proposed by Reid [3]_.
    Limited accuracy should be expected. Uncheecked.

    Examples
    --------
    >>> Sato_Riedel(300, 47, 390, 520)
    0.21037692461337687

    References
    ----------
    .. [1] Riedel, L.: Chem. Ing. Tech., 21, 349 (1949); 23: 59, 321, 465 (1951)
    .. [2] Maejima, T., private communication, 1973
    .. [3] Properties of Gases and Liquids", 3rd Ed., McGraw-Hill, 1977
    '''
    Tr = T/Tc
    Tbr = Tb/Tc
    return 1.1053*(3. + 20.*(1 - Tr)**(2/3.))*M**-0.5/(3. + 20.*(1 - Tbr)**(2/3.))