def Wilke(ys, mus, MWs):
    r'''Calculates viscosity of a gas mixture according to
    mixing rules in [1]_.

    .. math::
        \eta_{mix} = \sum_{i=1}^n \frac{y_i \eta_i}{\sum_{j=1}^n y_j \phi_{ij}}

        \phi_{ij} = \frac{(1 + \sqrt{\eta_i/\eta_j}(MW_j/MW_i)^{0.25})^2}
        {\sqrt{8(1+MW_i/MW_j)}}

    Parameters
    ----------
    ys : float
        Mole fractions of gas components
    mus : float
        Gas viscosities of all components, [Pa*S]
    MWs : float
        Molecular weights of all components, [g/mol]

    Returns
    -------
    mug : float
        Viscosity of gas mixture, Pa*S]

    Notes
    -----
    This equation is entirely dimensionless; all dimensions cancel.
    The original source has not been reviewed or found.

    Examples
    --------
    >>> Wilke([0.05, 0.95], [1.34E-5, 9.5029E-6], [64.06, 46.07])
    9.701614885866193e-06

    References
    ----------
    .. [1] TODO
    '''
    if not none_and_length_check([ys, mus, MWs]):  # check same-length inputs
        raise Exception('Function inputs are incorrect format')
    cmps = range(len(ys))
    phis = [[(1 + (mus[i]/mus[j])**0.5*(MWs[j]/MWs[i])**0.25)**2/(8*(1 + MWs[i]/MWs[j]))**0.5
                    for j in cmps] for i in cmps]

    return sum([ys[i]*mus[i]/sum([ys[j]*phis[i][j] for j in cmps]) for i in cmps])