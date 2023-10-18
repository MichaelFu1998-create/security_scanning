def Winterfeld_Scriven_Davis(xs, sigmas, rhoms):
    r'''Calculates surface tension of a liquid mixture according to
    mixing rules in [1]_ and also in [2]_.

    .. math::
        \sigma_M = \sum_i \sum_j \frac{1}{V_L^{L2}}\left(x_i V_i \right)
        \left( x_jV_j\right)\sqrt{\sigma_i\cdot \sigma_j}

    Parameters
    ----------
    xs : array-like
        Mole fractions of all components, [-]
    sigmas : array-like
        Surface tensions of all components, [N/m]
    rhoms : array-like
        Molar densities of all components, [mol/m^3]

    Returns
    -------
    sigma : float
        Air-liquid surface tension of mixture, [N/m]

    Notes
    -----
    DIPPR Procedure 7C: Method for the Surface Tension of Nonaqueous Liquid
    Mixtures

    Becomes less accurate as liquid-liquid critical solution temperature is
    approached. DIPPR Evaluation:  3-4% AARD, from 107 nonaqueous binary
    systems, 1284 points. Internally, densities are converted to kmol/m^3. The
    Amgat function is used to obtain liquid mixture density in this equation.

    Raises a ZeroDivisionError if either molar volume are zero, and a
    ValueError if a surface tensions of a pure component is negative.

    Examples
    --------
    >>> Winterfeld_Scriven_Davis([0.1606, 0.8394], [0.01547, 0.02877],
    ... [8610., 15530.])
    0.024967388450439824

    References
    ----------
    .. [1] Winterfeld, P. H., L. E. Scriven, and H. T. Davis. "An Approximate
       Theory of Interfacial Tensions of Multicomponent Systems: Applications
       to Binary Liquid-Vapor Tensions." AIChE Journal 24, no. 6
       (November 1, 1978): 1010-14. doi:10.1002/aic.690240610.
    .. [2] Danner, Ronald P, and Design Institute for Physical Property Data.
       Manual for Predicting Chemical Process Design Data. New York, N.Y, 1982.
    '''
    if not none_and_length_check([xs, sigmas, rhoms]):
        raise Exception('Function inputs are incorrect format')
    rhoms = [i*1E-3 for i in rhoms]
    Vms = [1./i for i in rhoms]
    rho = 1./mixing_simple(xs, Vms)
    cmps = range(len(xs))
    rho2 = rho*rho
    return sum([rho2*xs[i]/rhoms[i]*xs[j]/rhoms[j]*(sigmas[j]*sigmas[i])**0.5
                for i in cmps for j in cmps])