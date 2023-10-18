def Herning_Zipperer(zs, mus, MWs):
    r'''Calculates viscosity of a gas mixture according to
    mixing rules in [1]_.

    .. math::
        TODO

    Parameters
    ----------
    zs : float
        Mole fractions of components
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
    The original source has not been reviewed.

    Examples
    --------

    References
    ----------
    .. [1] Herning, F. and Zipperer, L,: "Calculation of the Viscosity of
       Technical Gas Mixtures from the Viscosity of Individual Gases, german",
       Gas u. Wasserfach (1936) 79, No. 49, 69.
    '''
    if not none_and_length_check([zs, mus, MWs]):  # check same-length inputs
        raise Exception('Function inputs are incorrect format')
    MW_roots = [MWi**0.5 for MWi in MWs]
    denominator = sum([zi*MW_root_i for zi, MW_root_i in zip(zs, MW_roots)])
    k = sum([zi*mui*MW_root_i for zi, mui, MW_root_i in zip(zs, mus, MW_roots)])
    return k/denominator