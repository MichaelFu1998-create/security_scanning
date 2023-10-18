def SNM0(T, Tc, Vc, omega, delta_SRK=None):
    r'''Calculates saturated liquid density using the Mchaweh, Moshfeghian
    model [1]_. Designed for simple calculations.

    .. math::
        V_s = V_c/(1+1.169\tau^{1/3}+1.818\tau^{2/3}-2.658\tau+2.161\tau^{4/3}

        \tau = 1-\frac{(T/T_c)}{\alpha_{SRK}}

        \alpha_{SRK} = [1 + m(1-\sqrt{T/T_C}]^2

        m = 0.480+1.574\omega-0.176\omega^2

    If the fit parameter `delta_SRK` is provided, the following is used:

    .. math::
        V_s = V_C/(1+1.169\tau^{1/3}+1.818\tau^{2/3}-2.658\tau+2.161\tau^{4/3})
        /\left[1+\delta_{SRK}(\alpha_{SRK}-1)^{1/3}\right]

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Vc : float
        Critical volume of fluid [m^3/mol]
    omega : float
        Acentric factor for fluid, [-]
    delta_SRK : float, optional
        Fitting parameter [-]

    Returns
    -------
    Vs : float
        Saturation liquid volume, [m^3/mol]

    Notes
    -----
    73 fit parameters have been gathered from the article.

    Examples
    --------
    Argon, without the fit parameter and with it. Tabulated result in Perry's
    is 3.4613e-05. The fit increases the error on this occasion.

    >>> SNM0(121, 150.8, 7.49e-05, -0.004)
    3.4402256402733416e-05
    >>> SNM0(121, 150.8, 7.49e-05, -0.004, -0.03259620)
    3.493288100008123e-05

    References
    ----------
    .. [1] Mchaweh, A., A. Alsaygh, Kh. Nasrifar, and M. Moshfeghian.
       "A Simplified Method for Calculating Saturated Liquid Densities."
       Fluid Phase Equilibria 224, no. 2 (October 1, 2004): 157-67.
       doi:10.1016/j.fluid.2004.06.054
    '''
    Tr = T/Tc
    m = 0.480 + 1.574*omega - 0.176*omega*omega
    alpha_SRK = (1. + m*(1. - Tr**0.5))**2
    tau = 1. - Tr/alpha_SRK

    rho0 = 1. + 1.169*tau**(1/3.) + 1.818*tau**(2/3.) - 2.658*tau + 2.161*tau**(4/3.)
    V0 = 1./rho0

    if not delta_SRK:
        return Vc*V0
    else:
        return Vc*V0/(1. + delta_SRK*(alpha_SRK - 1.)**(1/3.))