def Zabransky_cubic(T, a1, a2, a3, a4):
    r'''Calculates liquid heat capacity using the model developed in [1]_.

    .. math::
        \frac{C}{R}=\sum_{j=0}^3 A_{j+1} \left(\frac{T}{100}\right)^j

    Parameters
    ----------
    T : float
        Temperature [K]
    a1-a4 : float
        Coefficients

    Returns
    -------
    Cp : float
        Liquid heat capacity, [J/mol/K]

    Notes
    -----
    Most often form used in [1]_.
    Analytical integrals are available for this expression.

    Examples
    --------
    >>> Zabransky_cubic(298.15, 20.9634, -10.1344, 2.8253, -0.256738)
    75.31462591538556

    References
    ----------
    .. [1] Zabransky, M., V. Ruzicka Jr, V. Majer, and Eugene S. Domalski.
       Heat Capacity of Liquids: Critical Review and Recommended Values.
       2 Volume Set. Washington, D.C.: Amer Inst of Physics, 1996.
    '''
    T = T/100.
    return R*(((a4*T + a3)*T + a2)*T + a1)