def ionic_strength(mis, zis):
    r'''Calculate the ionic strength of a solution in one of two ways,
    depending on the inputs only. For Pitzer and Bromley models,
    `mis` should be molalities of each component. For eNRTL models,
    `mis` should be mole fractions of each electrolyte in the solution.
    This will sum to be much less than 1.

    .. math::
        I = \frac{1}{2} \sum M_i z_i^2

        I = \frac{1}{2} \sum x_i z_i^2

    Parameters
    ----------
    mis : list
        Molalities of each ion, or mole fractions of each ion [mol/kg or -]
    zis : list
        Charges of each ion [-]

    Returns
    -------
    I : float
        ionic strength, [?]

    Examples
    --------
    >>> ionic_strength([0.1393, 0.1393], [1, -1])
    0.1393

    References
    ----------
    .. [1] Chen, Chau-Chyun, H. I. Britt, J. F. Boston, and L. B. Evans. "Local
       Composition Model for Excess Gibbs Energy of Electrolyte Systems.
       Part I: Single Solvent, Single Completely Dissociated Electrolyte
       Systems." AIChE Journal 28, no. 4 (July 1, 1982): 588-96.
       doi:10.1002/aic.690280410
    .. [2] Gmehling, Jurgen. Chemical Thermodynamics: For Process Simulation.
       Weinheim, Germany: Wiley-VCH, 2012.
    '''
    return 0.5*sum([mi*zi*zi for mi, zi in zip(mis, zis)])