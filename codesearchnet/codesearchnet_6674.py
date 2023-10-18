def bubble_at_P(P, zs, vapor_pressure_eqns, fugacities=None, gammas=None):
    '''Calculates bubble point for a given pressure

    Parameters
    ----------
    P : float
        Pressure, [Pa]
    zs : list[float]
        Overall mole fractions of all species, [-]
    vapor_pressure_eqns : list[functions]
        Temperature dependent function for each specie, Returns Psat, [Pa]
    fugacities : list[float], optional
        fugacities of each species, defaults to list of ones, [-]
    gammas : list[float], optional
        gammas of each species, defaults to list of ones, [-]

    Returns
    -------
    Tbubble : float, optional
        Temperature of bubble point at pressure `P`, [K]

    '''

    def bubble_P_error(T):
        Psats = [VP(T) for VP in vapor_pressure_eqns]
        Pcalc = bubble_at_T(zs, Psats, fugacities, gammas)

        return P - Pcalc

    T_bubble = newton(bubble_P_error, 300)

    return T_bubble