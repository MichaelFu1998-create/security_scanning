def permittivity_IAPWS(T, rho):
    r'''Calculate the relative permittivity of pure water as a function of.
    temperature and density. Assumes the 1997 IAPWS [1]_ formulation.

    .. math::
        \epsilon(\rho, T) =\frac{1 + A + 5B + (9 + 2A + 18B + A^2 + 10AB + 
        9B^2)^{0.5}}{4(1-B)}
        
        A(\rho, T) = \frac{N_A\mu^2\rho g}{M\epsilon_0 kT}
        
        B(\rho) = \frac{N_A\alpha\rho}{3M\epsilon_0}
        
        g(\delta,\tau) = 1 + \sum_{i=1}^{11}n_i\delta^{I_i}\tau^{J_i} 
        + n_{12}\delta\left(\frac{647.096}{228}\tau^{-1} - 1\right)^{-1.2}

        \delta = \rho/(322 \text{ kg/m}^3)
        
        \tau = T/647.096\text{K}

    Parameters
    ----------
    T : float
        Temperature of water [K]
    rho : float
        Mass density of water at T and P [kg/m^3]

    Returns
    -------
    epsilon : float
        Relative permittivity of water at T and rho, [-]

    Notes
    -----
    Validity:
    
    273.15 < T < 323.15 K for 0 < P < iceVI melting pressure at T or 1000 MPa,
    whichever is smaller.
    
    323.15 < T < 873.15 K 0 < p < 600 MPa.
    
    Coefficients:
    
    ih = [1, 1, 1, 2, 3, 3, 4, 5, 6, 7, 10];
    jh = [0.25, 1, 2.5, 1.5, 1.5, 2.5, 2, 2, 5, 0.5, 10];
    Nh = [0.978224486826, -0.957771379375, 0.237511794148, 0.714692244396,
          -0.298217036956, -0.108863472196, 0.949327488264E-1, 
          -.980469816509E-2, 0.165167634970E-4, 0.937359795772E-4, 
          -0.12317921872E-9];
    polarizability = 1.636E-40
    dipole = 6.138E-30
    
    Examples
    --------
    >>> permittivity_IAPWS(373., 958.46)
    55.56584297721836

    References
    ----------
    .. [1] IAPWS. 1997. Release on the Static Dielectric Constant of Ordinary 
       Water Substance for Temperatures from 238 K to 873 K and Pressures up 
       to 1000 MPa.
    '''
    dipole = 6.138E-30 # actual molecular dipole moment of water, in C*m
    polarizability = 1.636E-40 # actual mean molecular polarizability of water, C^2/J*m^2
    MW = 0.018015268 # molecular weight of water, kg/mol
    ih = [1, 1, 1, 2, 3, 3, 4, 5, 6, 7, 10]
    jh = [0.25, 1, 2.5, 1.5, 1.5, 2.5, 2, 2, 5, 0.5, 10]
    Nh = [0.978224486826, -0.957771379375, 0.237511794148, 0.714692244396,
          -0.298217036956, -0.108863472196, 0.949327488264E-1, 
          -.980469816509E-2, 0.165167634970E-4, 0.937359795772E-4, 
          -0.12317921872E-9]
    
    delta = rho/322.
    tau = 647.096/T
    
    g = (1 + sum([Nh[h]*delta**ih[h]*tau**jh[h] for h in range(11)])
        + 0.196096504426E-2*delta*(T/228. - 1)**-1.2)
    
    A = N_A*dipole**2*(rho/MW)*g/epsilon_0/k/T
    B = N_A*polarizability*(rho/MW)/3./epsilon_0
    epsilon = (1. + A + 5.*B + (9. + 2.*A + 18.*B + A**2 + 10.*A*B + 9.*B**2
        )**0.5)/(4. - 4.*B)
    return epsilon