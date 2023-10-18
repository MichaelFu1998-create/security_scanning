def Chung(T, MW, Tc, omega, Cvm, mu):
    r'''Estimates the thermal conductivity of a gas as a function of
    temperature using the CSP method of Chung [1]_.

    .. math::
        \frac{\lambda M}{\eta C_v} = \frac{3.75 \Psi}{C_v/R}

        \Psi = 1 + \alpha \left\{[0.215+0.28288\alpha-1.061\beta+0.26665Z]/
        [0.6366+\beta Z + 1.061 \alpha \beta]\right\}

        \alpha = \frac{C_v}{R}-1.5

        \beta = 0.7862-0.7109\omega + 1.3168\omega^2

        Z=2+10.5T_r^2

    Parameters
    ----------
    T : float
        Temperature of the gas [K]
    MW : float
        Molecular weight of the gas [g/mol]
    Tc : float
        Critical temperature of the gas [K]
    omega : float
        Acentric factor of the gas [-]
    Cvm : float
        Molar contant volume heat capacity of the gas [J/mol/K]
    mu : float
        Gas viscosity [Pa*S]

    Returns
    -------
    kg : float
        Estimated gas thermal conductivity [W/m/k]

    Notes
    -----
    MW internally converted to kg/g-mol.

    Examples
    --------
    2-methylbutane at low pressure, 373.15 K. Mathes calculation in [2]_.

    >>> Chung(T=373.15, MW=72.151, Tc=460.4, omega=0.227, Cvm=135.9, mu=8.77E-6)
    0.023015653729496946

    References
    ----------
    .. [1] Chung, Ting Horng, Lloyd L. Lee, and Kenneth E. Starling.
       "Applications of Kinetic Gas Theories and Multiparameter Correlation for
       Prediction of Dilute Gas Viscosity and Thermal Conductivity."
       Industrial & Engineering Chemistry Fundamentals 23, no. 1
       (February 1, 1984): 8-13. doi:10.1021/i100013a002
    .. [2] Reid, Robert C.; Prausnitz, John M.; Poling, Bruce E.
       Properties of Gases and Liquids. McGraw-Hill Companies, 1987.
    '''
    MW = MW/1000.
    alpha = Cvm/R - 1.5
    beta = 0.7862 - 0.7109*omega + 1.3168*omega**2
    Z = 2 + 10.5*(T/Tc)**2
    psi = 1 + alpha*((0.215 + 0.28288*alpha - 1.061*beta + 0.26665*Z)
                      /(0.6366 + beta*Z + 1.061*alpha*beta))
    return 3.75*psi/(Cvm/R)/MW*mu*Cvm