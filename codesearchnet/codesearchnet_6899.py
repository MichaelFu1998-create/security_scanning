def Chueh_Prausnitz_Tc(zs, Tcs, Vcs, taus):
    r'''Calculates critical temperature of a mixture according to
    mixing rules in [1]_.

    .. math::
        T_{cm} = \sum_i^n \theta_i Tc_i + \sum_i^n\sum_j^n(\theta_i \theta_j
        \tau_{ij})T_{ref}

        \theta = \frac{x_i V_{ci}^{2/3}}{\sum_{j=1}^n x_j V_{cj}^{2/3}}

    For a binary mxiture, this simplifies to:

    .. math::
        T_{cm} = \theta_1T_{c1} + \theta_2T_{c2}  + 2\theta_1\theta_2\tau_{12}

    Parameters
    ----------
    zs : array-like
        Mole fractions of all components
    Tcs : array-like
        Critical temperatures of all components, [K]
    Vcs : array-like
        Critical volumes of all components, [m^3/mol]
    taus : array-like of shape `zs` by `zs`
        Interaction parameters

    Returns
    -------
    Tcm : float
        Critical temperatures of the mixture, [K]

    Notes
    -----
    All parameters, even if zero, must be given to this function.

    Examples
    --------
    butane/pentane/hexane 0.6449/0.2359/0.1192 mixture, exp: 450.22 K.

    >>> Chueh_Prausnitz_Tc([0.6449, 0.2359, 0.1192], [425.12, 469.7, 507.6],
    ... [0.000255, 0.000313, 0.000371], [[0, 1.92681, 6.80358],
    ... [1.92681, 0, 1.89312], [ 6.80358, 1.89312, 0]])
    450.1225764723492

    References
    ----------
    .. [1] Chueh, P. L., and J. M. Prausnitz. "Vapor-Liquid Equilibria at High
       Pressures: Calculation of Critical Temperatures, Volumes, and Pressures
       of Nonpolar Mixtures." AIChE Journal 13, no. 6 (November 1, 1967):
       1107-13. doi:10.1002/aic.690130613.
    .. [2] Najafi, Hamidreza, Babak Maghbooli, and Mohammad Amin Sobati.
       "Prediction of True Critical Temperature of Multi-Component Mixtures:
       Extending Fast Estimation Methods." Fluid Phase Equilibria 392
       (April 25, 2015): 104-26. doi:10.1016/j.fluid.2015.02.001.
    '''
    if not none_and_length_check([zs, Tcs, Vcs]):
        raise Exception('Function inputs are incorrect format')

    denominator = sum(zs[i]*Vcs[i]**(2/3.) for i in range(len(zs)))
    Tcm = 0
    for i in range(len(zs)):
        Tcm += zs[i]*Vcs[i]**(2/3.)*Tcs[i]/denominator
        for j in range(len(zs)):
            Tcm += (zs[i]*Vcs[i]**(2/3.)/denominator)*(zs[j]*Vcs[j]**(2/3.)/denominator)*taus[i][j]
    return Tcm