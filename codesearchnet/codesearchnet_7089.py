def eli_hanley(T, MW, Tc, Vc, Zc, omega, Cvm):
    r'''Estimates the thermal conductivity of a gas as a function of
    temperature using the reference fluid method of Eli and Hanley [1]_ as
    shown in [2]_.

    .. math::
        \lambda = \lambda^* + \frac{\eta^*}{MW}(1.32)\left(C_v - \frac{3R}{2}\right)

        Tr = \text{min}(Tr, 2)

        \theta = 1 + (\omega-0.011)\left(0.56553 - 0.86276\ln Tr - \frac{0.69852}{Tr}\right)

        \psi = [1 + (\omega - 0.011)(0.38560 - 1.1617\ln Tr)]\frac{0.288}{Z_c}

        f = \frac{T_c}{190.4}\theta

        h = \frac{V_c}{9.92E-5}\psi

        T_0 = T/f

        \eta_0^*(T_0)= \sum_{n=1}^9 C_n T_0^{(n-4)/3}

        \theta_0 = 1944 \eta_0

        \lambda^* = \lambda_0 H

        \eta^* = \eta^*_0 H \frac{MW}{16.04}

        H = \left(\frac{16.04}{MW}\right)^{0.5}f^{0.5}/h^{2/3}

    Parameters
    ----------
    T : float
        Temperature of the gas [K]
    MW : float
        Molecular weight of the gas [g/mol]
    Tc : float
        Critical temperature of the gas [K]
    Vc : float
        Critical volume of the gas [m^3/mol]
    Zc : float
        Critical compressibility of the gas []
    omega : float
        Acentric factor of the gas [-]
    Cvm : float
        Molar contant volume heat capacity of the gas [J/mol/K]

    Returns
    -------
    kg : float
        Estimated gas thermal conductivity [W/m/k]

    Notes
    -----
    Reference fluid is Methane.
    MW internally converted to kg/g-mol.

    Examples
    --------
    2-methylbutane at low pressure, 373.15 K. Mathes calculation in [2]_.

    >>> eli_hanley(T=373.15, MW=72.151, Tc=460.4, Vc=3.06E-4, Zc=0.267,
    ... omega=0.227, Cvm=135.9)
    0.02247951789135337

    References
    ----------
    .. [1] Ely, James F., and H. J. M. Hanley. "Prediction of Transport
       Properties. 2. Thermal Conductivity of Pure Fluids and Mixtures."
       Industrial & Engineering Chemistry Fundamentals 22, no. 1 (February 1,
       1983): 90-97. doi:10.1021/i100009a016.
    .. [2] Reid, Robert C.; Prausnitz, John M.; Poling, Bruce E.
       Properties of Gases and Liquids. McGraw-Hill Companies, 1987.
    '''
    Cs = [2.907741307E6, -3.312874033E6, 1.608101838E6, -4.331904871E5, 
          7.062481330E4, -7.116620750E3, 4.325174400E2, -1.445911210E1, 2.037119479E-1]

    Tr = T/Tc
    if Tr > 2: Tr = 2
    theta = 1 + (omega - 0.011)*(0.56553 - 0.86276*log(Tr) - 0.69852/Tr)
    psi = (1 + (omega-0.011)*(0.38560 - 1.1617*log(Tr)))*0.288/Zc
    f = Tc/190.4*theta
    h = Vc/9.92E-5*psi
    T0 = T/f
    eta0 = 1E-7*sum([Ci*T0**((i+1. - 4.)/3.) for i, Ci in enumerate(Cs)])
    k0 = 1944*eta0

    H = (16.04/MW)**0.5*f**0.5*h**(-2/3.)
    etas = eta0*H*MW/16.04
    ks = k0*H
    return ks + etas/(MW/1000.)*1.32*(Cvm - 1.5*R)