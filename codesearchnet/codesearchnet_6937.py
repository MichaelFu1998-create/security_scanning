def Przedziecki_Sridhar(T, Tm, Tc, Pc, Vc, Vm, omega, MW):
    r'''Calculates the viscosity of a liquid using an emperical formula
    developed in [1]_.

    .. math::
        \mu=\frac{V_o}{E(V-V_o)}

        E=-1.12+\frac{V_c}{12.94+0.10MW-0.23P_c+0.0424T_{m}-11.58(T_{m}/T_c)}

        V_o = 0.0085\omega T_c-2.02+\frac{V_{m}}{0.342(T_m/T_c)+0.894}

    Parameters
    ----------
    T : float
        Temperature of the fluid [K]
    Tm : float
        Melting point of fluid [K]
    Tc : float
        Critical temperature of the fluid [K]
    Pc : float
        Critical pressure of the fluid [Pa]
    Vc : float
        Critical volume of the fluid [m^3/mol]
    Vm : float
        Molar volume of the fluid at temperature [K]
    omega : float
        Acentric factor of compound
    MW : float
        Molwcular weight of fluid [g/mol]

    Returns
    -------
    mu_l : float
        Viscosity of liquid, [Pa*S]

    Notes
    -----
    A test by Reid (1983) is used, but only mostly correct.
    This function is not recommended. Its use has been removed from the Liquid Viscosity function.
    Internal units are bar and mL/mol.
    TODO: Test again with data from 5th ed table.

    Examples
    --------
    >>> Przedziecki_Sridhar(383., 178., 591.8, 41E5, 316E-6, 95E-6, .263, 92.14)
    0.0002198147995603383

    References
    ----------
    .. [1] Przedziecki, J. W., and T. Sridhar. "Prediction of Liquid
       Viscosities." AIChE Journal 31, no. 2 (February 1, 1985): 333-35.
       doi:10.1002/aic.690310225.
    '''
    Pc = Pc/1E5  # Pa to atm
    Vm, Vc = Vm*1E6, Vc*1E6  # m^3/mol to mL/mol
    Tr = T/Tc
    Gamma = 0.29607 - 0.09045*Tr - 0.04842*Tr**2
    VrT = 0.33593-0.33953*Tr + 1.51941*Tr**2 - 2.02512*Tr**3 + 1.11422*Tr**4
    V = VrT*(1-omega*Gamma)*Vc

    Vo = 0.0085*omega*Tc - 2.02 + Vm/(0.342*(Tm/Tc) + 0.894)  # checked
    E = -1.12 + Vc/(12.94 + 0.1*MW - 0.23*Pc + 0.0424*Tm - 11.58*(Tm/Tc))
    return Vo/(E*(V-Vo))/1000.