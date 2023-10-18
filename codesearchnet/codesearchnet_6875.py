def Pitzer(T, Tc, Pc, omega):
    r'''Calculates air-water surface tension using the correlation derived
    by [1]_ from the works of [2]_ and [3]_. Based on critical property CSP
    methods.

    .. math::
        \sigma = P_c^{2/3}T_c^{1/3}\frac{1.86 + 1.18\omega}{19.05}
        \left[ \frac{3.75 + 0.91 \omega}{0.291 - 0.08 \omega}\right]^{2/3} (1-T_r)^{11/9}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]
    omega : float
        Acentric factor for fluid, [-]

    Returns
    -------
    sigma : float
        Liquid surface tension, N/m

    Notes
    -----
    The source of this equation has not been reviewed.
    Internal units of presure are bar, surface tension of mN/m.

    Examples
    --------
    Chlorobenzene from Poling, as compared with a % error value at 293 K.

    >>> Pitzer(293., 633.0, 4530000.0, 0.249)
    0.03458453513446387

    References
    ----------
    .. [1] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
       New York: McGraw-Hill Professional, 2000.
    .. [2] Curl, R. F., and Kenneth Pitzer. "Volumetric and Thermodynamic
       Properties of Fluids-Enthalpy, Free Energy, and Entropy." Industrial &
       Engineering Chemistry 50, no. 2 (February 1, 1958): 265-74.
       doi:10.1021/ie50578a047
    .. [3] Pitzer, K. S.: Thermodynamics, 3d ed., New York, McGraw-Hill,
       1995, p. 521.
    '''
    Tr = T/Tc
    Pc = Pc/1E5  # Convert to bar
    sigma = Pc**(2/3.0)*Tc**(1/3.0)*(1.86+1.18*omega)/19.05 * (
        (3.75+0.91*omega)/(0.291-0.08*omega))**(2/3.0)*(1-Tr)**(11/9.0)
    sigma = sigma/1000  # N/m, please
    return sigma