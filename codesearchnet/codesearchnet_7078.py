def Nicola(T, M, Tc, Pc, omega):
    r'''Estimates the thermal conductivity of a liquid as a function of
    temperature using the CSP method of [1]_. A statistically derived
    equation using any correlated terms.

    Requires temperature, molecular weight, critical temperature and pressure,
    and acentric factor.

    .. math::
        \frac{\lambda}{0.5147 W/m/K} = -0.2537T_r+\frac{0.0017Pc}{\text{bar}}
        +0.1501 \omega + \left(\frac{1}{MW}\right)^{-0.2999}

    Parameters
    ----------
    T : float
        Temperature of the fluid [K]
    M : float
        Molecular weight of the fluid [g/mol]
    Tc : float
        Critical temperature of the fluid [K]
    Pc : float
        Critical pressure of the fluid [Pa]
    omega : float
        Acentric factor of the fluid [-]

    Returns
    -------
    kl : float
        Estimated liquid thermal conductivity [W/m/k]

    Notes
    -----
    A statistical correlation. A revision of an original correlation.

    Examples
    --------
    >>> Nicola(300, 142.3, 611.7, 2110000.0, 0.49)
    0.10863821554584034

    References
    ----------
    .. [1] Di Nicola, Giovanni, Eleonora Ciarrocchi, Gianluca Coccia, and
       Mariano Pierantozzi. "Correlations of Thermal Conductivity for
       Liquid Refrigerants at Atmospheric Pressure or near Saturation."
       International Journal of Refrigeration. 2014.
       doi:10.1016/j.ijrefrig.2014.06.003
    '''
    Tr = T/Tc
    Pc = Pc/1E5
    return 0.5147*(-0.2537*Tr + 0.0017*Pc + 0.1501*omega + (1./M)**0.2999)