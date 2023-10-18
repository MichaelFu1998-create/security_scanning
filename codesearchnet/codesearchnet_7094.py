def chung_dense(T, MW, Tc, Vc, omega, Cvm, Vm, mu, dipole, association=0):
    r'''Estimates the thermal conductivity of a gas at high pressure as a
    function of temperature using the reference fluid method of
    Chung [1]_ as shown in [2]_.

    .. math::
        \lambda = \frac{31.2 \eta^\circ \Psi}{M'}(G_2^{-1} + B_6 y)+qB_7y^2T_r^{1/2}G_2

        \Psi = 1 + \alpha \left\{[0.215+0.28288\alpha-1.061\beta+0.26665Z]/
        [0.6366+\beta Z + 1.061 \alpha \beta]\right\}

        \alpha = \frac{C_v}{R}-1.5

        \beta = 0.7862-0.7109\omega + 1.3168\omega^2

        Z=2+10.5T_r^2

        q = 3.586\times 10^{-3} (T_c/M')^{1/2}/V_c^{2/3}

        y = \frac{V_c}{6V}

        G_1 = \frac{1-0.5y}{(1-y)^3}

        G_2 = \frac{(B_1/y)[1-\exp(-B_4y)]+ B_2G_1\exp(B_5y) + B_3G_1}
        {B_1B_4 + B_2 + B_3}

        B_i = a_i + b_i \omega + c_i \mu_r^4 + d_i \kappa


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
    omega : float
        Acentric factor of the gas [-]
    Cvm : float
        Molar contant volume heat capacity of the gas [J/mol/K]
    Vm : float
        Molar volume of the gas at T and P [m^3/mol]
    mu : float
        Low-pressure gas viscosity [Pa*S]
    dipole : float
        Dipole moment [debye]
    association : float, optional
        Association factor [-]

    Returns
    -------
    kg : float
        Estimated dense gas thermal conductivity [W/m/k]

    Notes
    -----
    MW internally converted to kg/g-mol.
    Vm internally converted to mL/mol.
    [1]_ is not the latest form as presented in [1]_.
    Association factor is assumed 0. Relates to the polarity of the gas.

    Coefficients as follows:
    ais = [2.4166E+0, -5.0924E-1, 6.6107E+0, 1.4543E+1, 7.9274E-1, -5.8634E+0, 9.1089E+1]

    bis = [7.4824E-1, -1.5094E+0, 5.6207E+0, -8.9139E+0, 8.2019E-1, 1.2801E+1, 1.2811E+2]

    cis = [-9.1858E-1, -4.9991E+1, 6.4760E+1, -5.6379E+0, -6.9369E-1, 9.5893E+0, -5.4217E+1]

    dis = [1.2172E+2, 6.9983E+1, 2.7039E+1, 7.4344E+1, 6.3173E+0, 6.5529E+1, 5.2381E+2]


    Examples
    --------
    >>> chung_dense(T=473., MW=42.081, Tc=364.9, Vc=184.6E-6, omega=0.142,
    ... Cvm=82.67, Vm=172.1E-6, mu=134E-7, dipole=0.4)
    0.06160570379787278

    References
    ----------
    .. [1] Chung, Ting Horng, Mohammad Ajlan, Lloyd L. Lee, and Kenneth E.
       Starling. "Generalized Multiparameter Correlation for Nonpolar and Polar
       Fluid Transport Properties." Industrial & Engineering Chemistry Research
       27, no. 4 (April 1, 1988): 671-79. doi:10.1021/ie00076a024.
    .. [2] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
       New York: McGraw-Hill Professional, 2000.
    '''
    ais = [2.4166E+0, -5.0924E-1, 6.6107E+0, 1.4543E+1, 7.9274E-1, -5.8634E+0, 9.1089E+1]
    bis = [7.4824E-1, -1.5094E+0, 5.6207E+0, -8.9139E+0, 8.2019E-1, 1.2801E+1, 1.2811E+2]
    cis = [-9.1858E-1, -4.9991E+1, 6.4760E+1, -5.6379E+0, -6.9369E-1, 9.5893E+0, -5.4217E+1]
    dis = [1.2172E+2, 6.9983E+1, 2.7039E+1, 7.4344E+1, 6.3173E+0, 6.5529E+1, 5.2381E+2]
    Tr = T/Tc
    mur = 131.3*dipole/(Vc*1E6*Tc)**0.5

    # From Chung Method
    alpha = Cvm/R - 1.5
    beta = 0.7862 - 0.7109*omega + 1.3168*omega**2
    Z = 2 + 10.5*(T/Tc)**2
    psi = 1 + alpha*((0.215 + 0.28288*alpha - 1.061*beta + 0.26665*Z)/(0.6366 + beta*Z + 1.061*alpha*beta))

    y = Vc/(6*Vm)
    B1, B2, B3, B4, B5, B6, B7 = [ais[i] + bis[i]*omega + cis[i]*mur**4 + dis[i]*association for i in range(7)]
    G1 = (1 - 0.5*y)/(1. - y)**3
    G2 = (B1/y*(1 - exp(-B4*y)) + B2*G1*exp(B5*y) + B3*G1)/(B1*B4 + B2 + B3)
    q = 3.586E-3*(Tc/(MW/1000.))**0.5/(Vc*1E6)**(2/3.)
    return 31.2*mu*psi/(MW/1000.)*(G2**-1 + B6*y) + q*B7*y**2*Tr**0.5*G2