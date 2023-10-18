def collision_integral_Neufeld_Janzen_Aziz(Tstar, l=1, s=1):
    r'''Calculates Lennard-Jones collision integral for any of 16 values of
    (l,j) for the wide range of 0.3 < Tstar < 100. Values are accurate to
    0.1 % of actual values, but the calculation of actual values is
    computationally intensive and so these simplifications are used, developed
    in [1]_.

    .. math::
        \Omega_D = \frac{A}{T^{*B}} + \frac{C}{\exp(DT^*)} +
        \frac{E}{\exp(FT^{*})} + \frac{G}{\exp(HT^*)} + RT^{*B}\sin(ST^{*W}-P)

    Parameters
    ----------
    Tstar : float
        Reduced temperature of the fluid [-]
    l : int
        term
    s : int
        term

    Returns
    -------
    Omega : float
        Collision integral of A and B

    Notes
    -----
    Acceptable pairs of (l,s) are (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
    (1, 6), (1, 7), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 3), (3, 4),
    (3, 5), and (4, 4).

    .. math::
        T^* = \frac{k_b T}{\epsilon}

    Results are very similar to those of the more modern formulation,
    `collision_integral_Kim_Monroe`.

    Calculations begin to yield overflow errors in some values of (l, 2) after
    Tstar = 75, beginning with (1, 7). Also susceptible are (1, 5) and (1, 6).

    Examples
    --------
    >>> collision_integral_Neufeld_Janzen_Aziz(100, 1, 1)
    0.516717697672334

    References
    ----------
    .. [1] Neufeld, Philip D., A. R. Janzen, and R. A. Aziz. "Empirical
       Equations to Calculate 16 of the Transport Collision Integrals
       Omega(l, S)* for the Lennard-Jones (12-6) Potential." The Journal of
       Chemical Physics 57, no. 3 (August 1, 1972): 1100-1102.
       doi:10.1063/1.1678363
    '''
    if (l, s) not in Neufeld_collision:
        raise Exception('Input values of l and s are not supported')
    A, B, C, D, E, F, G, H, R, S, W, P = Neufeld_collision[(l, s)]
    omega = A/Tstar**B + C/exp(D*Tstar) + E/exp(F*Tstar)
    if (l, s) in [(1, 1), (1, 2), (3, 3)]:
        omega += G/exp(H*Tstar)
    if (l, s) not in [(1, 1), (1, 2)]:
        omega += R*Tstar**B*sin(S*Tstar**W-P)
    return omega