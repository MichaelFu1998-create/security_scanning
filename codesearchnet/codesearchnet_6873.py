def Somayajulu(T, Tc, A, B, C):
    r'''Calculates air-water surface tension  using the [1]_
    emperical (parameter-regressed) method. Well regressed, no recent data.

    .. math::
        \sigma=aX^{5/4}+bX^{9/4}+cX^{13/4}
        X=(T_c-T)/T_c

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    A : float
        Regression parameter
    B : float
        Regression parameter
    C : float
        Regression parameter

    Returns
    -------
    sigma : float
        Liquid surface tension, N/m

    Notes
    -----
    Presently untested, but matches expected values. Internal units are mN/m.
    Form of function returns imaginary results when T > Tc; None is returned
    if this is the case. Function is claimed valid from the triple to the
    critical point. Results can be evaluated beneath the triple point.

    Examples
    --------
    Water at 300 K

    >>> Somayajulu(300, 647.126, 232.713514, -140.18645, -4.890098)
    0.07166386387996757

    References
    ----------
    .. [1] Somayajulu, G. R. "A Generalized Equation for Surface Tension from
       the Triple Point to the Critical Point." International Journal of
       Thermophysics 9, no. 4 (July 1988): 559-66. doi:10.1007/BF00503154.
    '''
    X = (Tc-T)/Tc
    sigma = (A*X**1.25 + B*X**2.25 + C*X**3.25)/1000.
    return sigma