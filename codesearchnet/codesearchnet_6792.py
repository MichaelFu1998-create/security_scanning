def Chen(Tb, Tc, Pc):
    r'''Calculates enthalpy of vaporization using the Chen [1]_ correlation
    and a chemical's critical temperature, pressure and boiling point.

    The enthalpy of vaporization is given by:

    .. math::
        \Delta H_{vb} = RT_b \frac{3.978 T_r - 3.958 + 1.555 \ln P_c}{1.07 - T_r}

    Parameters
    ----------
    Tb : float
        Boiling temperature of the fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]

    Returns
    -------
    Hvap : float
        Enthalpy of vaporization, [J/mol]

    Notes
    -----
    The formulation presented in the original article is similar, but uses
    units of atm and calorie instead. The form in [2]_ has adjusted for this.
    A method for estimating enthalpy of vaporization at other conditions
    has also been developed, but the article is unclear on its implementation.
    Based on the Pitzer correlation.

    Internal units: bar and K

    Examples
    --------
    Same problem as in Perry's examples.

    >>> Chen(294.0, 466.0, 5.55E6)
    26705.893506174052

    References
    ----------
    .. [1] Chen, N. H. "Generalized Correlation for Latent Heat of Vaporization."
       Journal of Chemical & Engineering Data 10, no. 2 (April 1, 1965): 207-10.
       doi:10.1021/je60025a047
    .. [2] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
       New York: McGraw-Hill Professional, 2000.
    '''
    Tbr = Tb/Tc
    Pc = Pc/1E5  # Pa to bar
    return R*Tb*(3.978*Tbr - 3.958 + 1.555*log(Pc))/(1.07 - Tbr)