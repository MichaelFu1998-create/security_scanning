def Li_Johns_Ahmadi_solution(zs, Ks):
    r'''Solves the objective function of the Li-Johns-Ahmadi flash equation.
    Uses the method proposed in [1]_ to obtain an initial guess.

    .. math::
        0 = 1 + \left(\frac{K_{max}-K_{min}}{K_{min}-1}\right)x_1
        + \sum_{i=2}^{n-1}\frac{K_i-K_{min}}{K_{min}-1}\left[\frac{z_i(K_{max}
        -1)x_{max}}{(K_i-1)z_{max} + (K_{max}-K_i)x_{max}}\right]

    Parameters
    ----------
    zs : list[float]
        Overall mole fractions of all species, [-]
    Ks : list[float]
        Equilibrium K-values, [-]

    Returns
    -------
    V_over_F : float
        Vapor fraction solution [-]
    xs : list[float]
        Mole fractions of each species in the liquid phase, [-]
    ys : list[float]
        Mole fractions of each species in the vapor phase, [-]

    Notes
    -----
    The initial guess is the average of the following, as described in [1]_.
    Each guess should be limited to be between 0 and 1 as they are often
    negative or larger than 1. `max` refers to the corresponding mole fractions
    for the species with the largest K value.

    .. math::
        \left(\frac{1-K_{min}}{K_{max}-K_{min}}\right)z_{max}\le x_{max} \le
        \left(\frac{1-K_{min}}{K_{max}-K_{min}}\right)

    If the `newton` method does not converge, a bisection method (brenth) is
    used instead. However, it is somewhat slower, especially as newton will
    attempt 50 iterations before giving up.

    This method does not work for problems of only two components.
    K values are sorted internally. Has not been found to be quicker than the
    Rachford-Rice equation.

    Examples
    --------
    >>> Li_Johns_Ahmadi_solution(zs=[0.5, 0.3, 0.2], Ks=[1.685, 0.742, 0.532])
    (0.6907302627738544, [0.33940869696634357, 0.3650560590371706, 0.2955352439964858], [0.5719036543882889, 0.27087159580558057, 0.15722474980613044])

    References
    ----------
    .. [1] Li, Yinghui, Russell T. Johns, and Kaveh Ahmadi. "A Rapid and Robust
       Alternative to Rachford-Rice in Flash Calculations." Fluid Phase
       Equilibria 316 (February 25, 2012): 85-97.
       doi:10.1016/j.fluid.2011.12.005.
    '''
    # Re-order both Ks and Zs by K value, higher coming first
    p = sorted(zip(Ks,zs), reverse=True)
    Ks_sorted, zs_sorted = [K for (K,z) in p], [z for (K,z) in p]


    # Largest K value and corresponding overall mole fraction
    k1 = Ks_sorted[0]
    z1 = zs_sorted[0]
    # Smallest K value
    kn = Ks_sorted[-1]

    x_min = (1. - kn)/(k1 - kn)*z1
    x_max = (1. - kn)/(k1 - kn)

    x_min2 = max(0., x_min)
    x_max2 = min(1., x_max)

    x_guess = (x_min2 + x_max2)*0.5

    length = len(zs)-1
    kn_m_1 = kn-1.
    k1_m_1 = (k1-1.)
    t1 = (k1-kn)/(kn-1.)

    objective = lambda x1: 1. + t1*x1 + sum([(ki-kn)/(kn_m_1) * zi*k1_m_1*x1 /( (ki-1.)*z1 + (k1-ki)*x1) for ki, zi in zip(Ks_sorted[1:length], zs_sorted[1:length])])
    try:
        x1 = newton(objective, x_guess)
        # newton skips out of its specified range in some cases, finding another solution
        # Check for that with asserts, and use brenth if it did
        # Must also check that V_over_F is right.
        assert x1 >= x_min2
        assert x1 <= x_max2
        V_over_F = (-x1 + z1)/(x1*(k1 - 1.))
        assert 0 <= V_over_F <= 1
    except:
        x1 = brenth(objective, x_min, x_max)
        V_over_F = (-x1 + z1)/(x1*(k1 - 1.))
    xs = [zi/(1.+V_over_F*(Ki-1.)) for zi, Ki in zip(zs, Ks)]
    ys = [Ki*xi for xi, Ki in zip(xs, Ks)]
    return V_over_F, xs, ys