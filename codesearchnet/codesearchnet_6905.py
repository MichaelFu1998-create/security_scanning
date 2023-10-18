def modified_Wilson_Vc(zs, Vcs, Aijs):
    r'''Calculates critical volume of a mixture according to
    mixing rules in [1]_ with parameters. Equation

    .. math::
        V_{cm} = \sum_i x_i V_{ci} + C\sum_i x_i \ln \left(x_i + \sum_j x_j A_{ij}\right)V_{ref}

    For a binary mxiture, this simplifies to:

    .. math::
        V_{cm} = x_1 V_{c1} + x_2 V_{c2} + C[x_1 \ln(x_1 + x_2A_{12}) + x_2\ln(x_2 + x_1 A_{21})]

    Parameters
    ----------
    zs : float
        Mole fractions of all components
    Vcs : float
        Critical volumes of all components, [m^3/mol]
    Aijs : matrix
        Interaction parameters, [cm^3/mol]

    Returns
    -------
    Vcm : float
        Critical volume of the mixture, [m^3/mol]

    Notes
    -----
    The equation and original article has been reviewed.
    All parameters, even if zero, must be given to this function.
    C = -2500

    All parameters, even if zero, must be given to this function.
    nu parameters are in cm^3/mol, but are converted to m^3/mol inside the function


    Examples
    --------
    1-butanol/benzene 0.4271/0.5729 mixture, Vcm = 268.096 mL/mol.

    >>> modified_Wilson_Vc([0.4271, 0.5729], [0.000273, 0.000256],
    ... [[0, 0.6671250], [1.3939900, 0]])
    0.0002664335032706881

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
    if not none_and_length_check([zs, Vcs]): # check same-length inputs
        raise Exception('Function inputs are incorrect format')
    C = -2500
    Vcm = sum(zs[i]*Vcs[i] for i in range(len(zs)))
    for i in range(len(zs)):
            Vcm += C*zs[i]*log(zs[i] + sum(zs[j]*Aijs[i][j] for j in range(len(zs))))/1E6
    return Vcm