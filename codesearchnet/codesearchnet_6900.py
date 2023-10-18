def Grieves_Thodos(zs, Tcs, Aijs):
    r'''Calculates critical temperature of a mixture according to
    mixing rules in [1]_.

    .. math::
        T_{cm} = \sum_{i} \frac{T_{ci}}{1 + (1/x_i)\sum_j A_{ij} x_j}

    For a binary mxiture, this simplifies to:

    .. math::
        T_{cm} = \frac{T_{c1}}{1 + (x_2/x_1)A_{12}} +  \frac{T_{c2}}
        {1 + (x_1/x_2)A_{21}}

    Parameters
    ----------
    zs : array-like
        Mole fractions of all components
    Tcs : array-like
        Critical temperatures of all components, [K]
    Aijs : array-like of shape `zs` by `zs`
        Interaction parameters

    Returns
    -------
    Tcm : float
        Critical temperatures of the mixture, [K]

    Notes
    -----
    All parameters, even if zero, must be given to this function.
    Giving 0s gives really bad results however.

    Examples
    --------
    butane/pentane/hexane 0.6449/0.2359/0.1192 mixture, exp: 450.22 K.

    >>> Grieves_Thodos([0.6449, 0.2359, 0.1192], [425.12, 469.7, 507.6], [[0, 1.2503, 1.516], [0.799807, 0, 1.23843], [0.659633, 0.807474, 0]])
    450.1839618758971

    References
    ----------
    .. [1] Grieves, Robert B., and George Thodos. "The Critical Temperatures of
       Multicomponent Hydrocarbon Systems." AIChE Journal 8, no. 4
       (September 1, 1962): 550-53. doi:10.1002/aic.690080426.
    .. [2] Najafi, Hamidreza, Babak Maghbooli, and Mohammad Amin Sobati.
       "Prediction of True Critical Temperature of Multi-Component Mixtures:
       Extending Fast Estimation Methods." Fluid Phase Equilibria 392
       (April 25, 2015): 104-26. doi:10.1016/j.fluid.2015.02.001.
    '''
    if not none_and_length_check([zs, Tcs]):
        raise Exception('Function inputs are incorrect format')
    Tcm = 0
    for i in range(len(zs)):
            Tcm += Tcs[i]/(1. + 1./zs[i]*sum(Aijs[i][j]*zs[j] for j in range(len(zs))))
    return Tcm