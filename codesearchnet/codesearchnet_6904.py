def Chueh_Prausnitz_Vc(zs, Vcs, nus):
    r'''Calculates critical volume of a mixture according to
    mixing rules in [1]_ with an interaction parameter.

    .. math::
        V_{cm} = \sum_i^n \theta_i V_{ci} + \sum_i^n\sum_j^n(\theta_i \theta_j \nu_{ij})V_{ref}
        \theta = \frac{x_i V_{ci}^{2/3}}{\sum_{j=1}^n x_j V_{cj}^{2/3}}

    Parameters
    ----------
    zs : float
        Mole fractions of all components
    Vcs : float
        Critical volumes of all components, [m^3/mol]
    nus : matrix
        Interaction parameters, [cm^3/mol]

    Returns
    -------
    Vcm : float
        Critical volume of the mixture, [m^3/mol]

    Notes
    -----
    All parameters, even if zero, must be given to this function.
    nu parameters are in cm^3/mol, but are converted to m^3/mol inside the function


    Examples
    --------
    1-butanol/benzene 0.4271/0.5729 mixture, Vcm = 268.096 mL/mol.

    >>> Chueh_Prausnitz_Vc([0.4271, 0.5729], [0.000273, 0.000256], [[0, 5.61847], [5.61847, 0]])
    0.00026620503424517445

    References
    ----------
    .. [1] Chueh, P. L., and J. M. Prausnitz. "Vapor-Liquid Equilibria at High
       Pressures: Calculation of Critical Temperatures, Volumes, and Pressures
       of Nonpolar Mixtures." AIChE Journal 13, no. 6 (November 1, 1967):
       1107-13. doi:10.1002/aic.690130613.
    .. [2] Najafi, Hamidreza, Babak Maghbooli, and Mohammad Amin Sobati.
       "Prediction of True Critical Volume of Multi-Component Mixtures:
       Extending Fast Estimation Methods." Fluid Phase Equilibria 386
       (January 25, 2015): 13-29. doi:10.1016/j.fluid.2014.11.008.
    '''
    if not none_and_length_check([zs, Vcs]): # check same-length inputs
        raise Exception('Function inputs are incorrect format')

    denominator = sum(zs[i]*Vcs[i]**(2/3.) for i in range(len(zs)))
    Vcm = 0
    for i in range(len(zs)):
        Vcm += zs[i]*Vcs[i]**(2/3.)*Vcs[i]/denominator
        for j in range(len(zs)):
            Vcm += (zs[i]*Vcs[i]**(2/3.)/denominator)*(zs[j]*Vcs[j]**(2/3.)/denominator)*nus[i][j]/1E6
    return Vcm