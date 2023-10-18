def collision_integral_Kim_Monroe(Tstar, l=1, s=1):
    r'''Calculates Lennard-Jones collision integral for any of 16 values of
    (l,j) for the wide range of 0.3 < Tstar < 400. Values are accurate to
    0.007 % of actual values, but the calculation of actual values is
    computationally intensive and so these simplifications are used, developed
    in [1]_.

    .. math::
        \Omega^{(l,s)*} = A^{(l,s)} + \sum_{k=1}^6 \left[ \frac{B_k^{(l,s)}}
        {(T^*)^k} + C_k^{(l,s)} (\ln T^*)^k \right]

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

    Examples
    --------
    >>> collision_integral_Kim_Monroe(400, 1, 1)
    0.4141818082392228

    References
    ----------
    .. [1] Kim, Sun Ung, and Charles W. Monroe. "High-Accuracy Calculations of
       Sixteen Collision Integrals for Lennard-Jones (12-6) Gases and Their
       Interpolation to Parameterize Neon, Argon, and Krypton." Journal of
       Computational Physics 273 (September 15, 2014): 358-73.
       doi:10.1016/j.jcp.2014.05.018.
    '''
    if (l, s) not in As_collision:
        raise Exception('Input values of l and s are not supported')
    omega = As_collision[(l, s)]
    for ki in range(6):
        Bs = Bs_collision[(l, s)]
        Cs = Cs_collision[(l, s)]
        omega += Bs[ki]/Tstar**(ki+1) + Cs[ki]*log(Tstar)**(ki+1)
    return omega