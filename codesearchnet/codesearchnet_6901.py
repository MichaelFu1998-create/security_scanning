def modified_Wilson_Tc(zs, Tcs, Aijs):
    r'''Calculates critical temperature of a mixture according to
    mixing rules in [1]_. Equation

    .. math::
        T_{cm} = \sum_i x_i T_{ci} + C\sum_i x_i \ln \left(x_i + \sum_j x_j A_{ij}\right)T_{ref}

    For a binary mxiture, this simplifies to:

    .. math::
        T_{cm} = x_1 T_{c1} + x_2 T_{c2} + C[x_1 \ln(x_1 + x_2A_{12}) + x_2\ln(x_2 + x_1 A_{21})]

    Parameters
    ----------
    zs : float
        Mole fractions of all components
    Tcs : float
        Critical temperatures of all components, [K]
    Aijs : matrix
        Interaction parameters

    Returns
    -------
    Tcm : float
        Critical temperatures of the mixture, [K]

    Notes
    -----
    The equation and original article has been reviewed.
    [1]_ has 75 binary systems, and additional multicomponent mixture parameters.
    All parameters, even if zero, must be given to this function.

    2rd example is from [2]_, for:
    butane/pentane/hexane 0.6449/0.2359/0.1192 mixture, exp: 450.22 K.
    Its result is identical to that calculated in the article.

    Examples
    --------
    >>> modified_Wilson_Tc([0.6449, 0.2359, 0.1192], [425.12, 469.7, 507.6],
    ... [[0, 1.174450, 1.274390], [0.835914, 0, 1.21038],
    ... [0.746878, 0.80677, 0]])
    450.0305966823031

    References
    ----------
    .. [1] Teja, Amyn S., Kul B. Garg, and Richard L. Smith. "A Method for the
       Calculation of Gas-Liquid Critical Temperatures and Pressures of
       Multicomponent Mixtures." Industrial & Engineering Chemistry Process
       Design and Development 22, no. 4 (1983): 672-76.
    .. [2] Najafi, Hamidreza, Babak Maghbooli, and Mohammad Amin Sobati.
       "Prediction of True Critical Temperature of Multi-Component Mixtures:
       Extending Fast Estimation Methods." Fluid Phase Equilibria 392
       (April 25, 2015): 104-26. doi:10.1016/j.fluid.2015.02.001.
    '''
    if not none_and_length_check([zs, Tcs]):
        raise Exception('Function inputs are incorrect format')
    C = -2500
    Tcm = sum(zs[i]*Tcs[i] for i in range(len(zs)))
    for i in range(len(zs)):
            Tcm += C*zs[i]*log(zs[i] + sum(zs[j]*Aijs[i][j] for j in range(len(zs))))
    return Tcm