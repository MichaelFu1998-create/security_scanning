def eli_hanley_dense(T, MW, Tc, Vc, Zc, omega, Cvm, Vm):
    r'''Estimates the thermal conductivity of a gas at high pressure as a
    function of temperature using the reference fluid method of Eli and
    Hanley [1]_ as shown in [2]_.

    .. math::
        Tr = min(Tr, 2)

        Vr = min(Vr, 2)

        f = \frac{T_c}{190.4}\theta

        h = \frac{V_c}{9.92E-5}\psi

        T_0 = T/f

        \rho_0 = \frac{16.04}{V}h

        \theta = 1 + (\omega-0.011)\left(0.09057 - 0.86276\ln Tr + \left(
        0.31664 - \frac{0.46568}{Tr}\right) (V_r - 0.5)\right)

        \psi = [1 + (\omega - 0.011)(0.39490(V_r - 1.02355) - 0.93281(V_r -
        0.75464)\ln T_r]\frac{0.288}{Z_c}

        \lambda_1 = 1944 \eta_0

        \lambda_2 = \left\{b_1 + b_2\left[b_3 - \ln \left(\frac{T_0}{b_4}
        \right)\right]^2\right\}\rho_0

        \lambda_3 = \exp\left(a_1 + \frac{a_2}{T_0}\right)\left\{\exp[(a_3 +
        \frac{a_4}{T_0^{1.5}})\rho_0^{0.1} + (\frac{\rho_0}{0.1617} - 1)
        \rho_0^{0.5}(a_5 + \frac{a_6}{T_0} + \frac{a_7}{T_0^2})] - 1\right\}

        \lambda^{**} = [\lambda_1 + \lambda_2 + \lambda_3]H

        H = \left(\frac{16.04}{MW}\right)^{0.5}f^{0.5}/h^{2/3}

        X = \left\{\left[1 - \frac{T}{f}\left(\frac{df}{dT}\right)_v \right]
        \frac{0.288}{Z_c}\right\}^{1.5}

        \left(\frac{df}{dT}\right)_v = \frac{T_c}{190.4}\left(\frac{d\theta}
        {d T}\right)_v

        \left(\frac{d\theta}{d T}\right)_v = (\omega-0.011)\left[
        \frac{-0.86276}{T} + (V_r-0.5)\frac{0.46568T_c}{T^2}\right]

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
    Vm : float
        Volume of the gas at T and P [m^3/mol]

    Returns
    -------
    kg : float
        Estimated dense gas thermal conductivity [W/m/k]

    Notes
    -----
    Reference fluid is Methane.
    MW internally converted to kg/g-mol.

    Examples
    --------
    >>> eli_hanley_dense(T=473., MW=42.081, Tc=364.9, Vc=1.81E-4, Zc=0.274,
    ... omega=0.144, Cvm=82.70, Vm=1.721E-4)
    0.06038475936515042

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
          7.062481330E4, -7.116620750E3, 4.325174400E2, -1.445911210E1,
          2.037119479E-1]

    Tr = T/Tc
    if Tr > 2:
        Tr = 2
    Vr = Vm/Vc
    if Vr > 2:
        Vr = 2
    theta = 1 + (omega - 0.011)*(0.09057 - 0.86276*log(Tr) + (0.31664 - 0.46568/Tr)*(Vr-0.5))
    psi = (1 + (omega-0.011)*(0.39490*(Vr-1.02355) - 0.93281*(Vr-0.75464)*log(Tr)))*0.288/Zc
    f = Tc/190.4*theta
    h = Vc/9.92E-5*psi
    T0 = T/f
    rho0 = 16.04/(Vm*1E6)*h  # Vm must be in cm^3/mol here.
    eta0 = 1E-7*sum([Cs[i]*T0**((i+1-4)/3.) for i in range(len(Cs))])
    k1 = 1944*eta0
    b1 = -0.25276920E0
    b2 = 0.334328590E0
    b3 = 1.12
    b4 = 0.1680E3
    k2 = (b1 + b2*(b3 - log(T0/b4))**2)/1000.*rho0

    a1 = -7.19771
    a2 = 85.67822
    a3 = 12.47183
    a4 = -984.6252
    a5 = 0.3594685
    a6 = 69.79841
    a7 = -872.8833

    k3 = exp(a1 + a2/T0)*(exp((a3 + a4/T0**1.5)*rho0**0.1 + (rho0/0.1617 - 1)*rho0**0.5*(a5 + a6/T0 + a7/T0**2)) - 1)/1000.

    if T/Tc > 2:
        dtheta = 0
    else:
        dtheta = (omega - 0.011)*(-0.86276/T + (Vr-0.5)*0.46568*Tc/T**2)
    dfdT = Tc/190.4*dtheta
    X = ((1 - T/f*dfdT)*0.288/Zc)**1.5

    H = (16.04/MW)**0.5*f**0.5/h**(2/3.)
    ks = (k1*X + k2 + k3)*H

    ### Uses calculations similar to those for pure species here
    theta = 1 + (omega - 0.011)*(0.56553 - 0.86276*log(Tr) - 0.69852/Tr)
    psi = (1 + (omega-0.011)*(0.38560 - 1.1617*log(Tr)))*0.288/Zc
    f = Tc/190.4*theta
    h = Vc/9.92E-5*psi
    T0 = T/f
    eta0 = 1E-7*sum([Cs[i]*T0**((i+1-4)/3.) for i in range(len(Cs))])
    H = (16.04/MW)**0.5*f**0.5/h**(2/3.)
    etas = eta0*H*MW/16.04
    k = ks + etas/(MW/1000.)*1.32*(Cvm-3*R/2.)
    return k