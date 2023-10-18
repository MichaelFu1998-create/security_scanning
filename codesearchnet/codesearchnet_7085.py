def Eucken(MW, Cvm, mu):
    r'''Estimates the thermal conductivity of a gas as a function of
    temperature using the CSP method of Eucken [1]_.

    .. math::
        \frac{\lambda M}{\eta C_v} = 1 + \frac{9/4}{C_v/R}

    Parameters
    ----------
    MW : float
        Molecular weight of the gas [g/mol]
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
    Temperature dependence is introduced via heat capacity and viscosity.
    A theoretical equation. No original author located.
    MW internally converted to kg/g-mol.

    Examples
    --------
    2-methylbutane at low pressure, 373.15 K. Mathes calculation in [1]_.

    >>> Eucken(MW=72.151, Cvm=135.9, mu=8.77E-6)
    0.018792644287722975

    References
    ----------
    .. [1] Reid, Robert C.; Prausnitz, John M.; Poling, Bruce E.
       Properties of Gases and Liquids. McGraw-Hill Companies, 1987.
    '''
    MW = MW/1000.
    return (1. + 9/4./(Cvm/R))*mu*Cvm/MW