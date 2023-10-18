def SMK(T, Tc, omega):
    r'''Calculates enthalpy of vaporization at arbitrary temperatures using a
    the work of [1]_; requires a chemical's critical temperature and
    acentric factor.

    The enthalpy of vaporization is given by:

    .. math::
         \frac{\Delta H_{vap}} {RT_c} =
         \left( \frac{\Delta H_{vap}} {RT_c} \right)^{(R1)} + \left(
         \frac{\omega - \omega^{(R1)}} {\omega^{(R2)} - \omega^{(R1)}} \right)
         \left[\left( \frac{\Delta H_{vap}} {RT_c} \right)^{(R2)} - \left(
         \frac{\Delta H_{vap}} {RT_c} \right)^{(R1)} \right]

        \left( \frac{\Delta H_{vap}} {RT_c} \right)^{(R1)}
        = 6.537 \tau^{1/3} - 2.467 \tau^{5/6} - 77.251 \tau^{1.208} +
        59.634 \tau + 36.009 \tau^2 - 14.606 \tau^3

        \left( \frac{\Delta H_{vap}} {RT_c} \right)^{(R2)} - \left(
        \frac{\Delta H_{vap}} {RT_c} \right)^{(R1)}=-0.133 \tau^{1/3} - 28.215
        \tau^{5/6} - 82.958 \tau^{1.208} + 99.00 \tau  + 19.105 \tau^2 -2.796 \tau^3

        \tau = 1-T/T_c

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    omega : float
        Acentric factor [-]

    Returns
    -------
    Hvap : float
        Enthalpy of vaporization, [J/mol]

    Notes
    -----
    The original article has been reviewed and found to have coefficients with
    slightly more precision. Additionally, the form of the equation is slightly
    different, but numerically equivalent.

    The refence fluids are:

    :math:`\omega_0` = benzene = 0.212

    :math:`\omega_1` = carbazole = 0.461

    A sample problem in the article has been verified. The numerical result
    presented by the author requires high numerical accuracy to obtain.

    Examples
    --------
    Problem in [1]_:

    >>> SMK(553.15, 751.35, 0.302)
    39866.17647797959

    References
    ----------
    .. [1] Sivaraman, Alwarappa, Joe W. Magee, and Riki Kobayashi. "Generalized
       Correlation of Latent Heats of Vaporization of Coal-Liquid Model Compounds
       between Their Freezing Points and Critical Points." Industrial &
       Engineering Chemistry Fundamentals 23, no. 1 (February 1, 1984): 97-100.
       doi:10.1021/i100013a017.
    '''
    omegaR1, omegaR2 = 0.212, 0.461
    A10 = 6.536924
    A20 = -2.466698
    A30 = -77.52141
    B10 = 59.63435
    B20 = 36.09887
    B30 = -14.60567

    A11 = -0.132584
    A21 = -28.21525
    A31 = -82.95820
    B11 = 99.00008
    B21 = 19.10458
    B31 = -2.795660

    tau = 1. - T/Tc
    L0 = A10*tau**(1/3.) + A20*tau**(5/6.) + A30*tau**(1-1/8. + 1/3.) + \
        B10*tau + B20*tau**2 + B30*tau**3

    L1 = A11*tau**(1/3.) + A21*tau**(5/6.0) + A31*tau**(1-1/8. + 1/3.) + \
        B11*tau + B21*tau**2 + B31*tau**3

    domega = (omega - omegaR1)/(omegaR2 - omegaR1)
    return R*Tc*(L0 + domega*L1)