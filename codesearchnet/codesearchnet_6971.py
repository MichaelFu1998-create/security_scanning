def Suzuki_LFL(Hc=None):
    r'''Calculates lower flammability limit, using the Suzuki [1]_ correlation.
    Uses heat of combustion only.

    The lower flammability limit of a gas is air is:

    .. math::
        \text{LFL} = \frac{-3.42}{\Delta H_c^{\circ}} + 0.569
        \Delta H_c^{\circ} + 0.0538\Delta H_c^{\circ 2} + 1.80

    Parameters
    ----------
    Hc : float
        Heat of combustion of gas [J/mol]

    Returns
    -------
    LFL : float
        Lower flammability limit, mole fraction [-]

    Notes
    -----
    Fit performed with 112 compounds, r^2 was 0.977.
    LFL in percent volume in air. Hc is at standard conditions, in MJ/mol.
    11 compounds left out as they were outliers.
    Equation does not apply for molecules with halogen atoms, only hydrocarbons
    with oxygen or nitrogen or sulfur.
    No sample calculation provided with the article. However, the equation is
    straightforward.

    Limits of equations's validity are -6135596 J where it predicts a
    LFL of 0, and -48322129 J where it predicts a LFL of 1.

    Examples
    --------
    Pentane, 1.5 % LFL in literature

    >>> Suzuki_LFL(-3536600)
    0.014276107095811815

    References
    ----------
    .. [1] Suzuki, Takahiro. "Note: Empirical Relationship between Lower
       Flammability Limits and Standard Enthalpies of Combustion of Organic
       Compounds." Fire and Materials 18, no. 5 (September 1, 1994): 333-36.
       doi:10.1002/fam.810180509.
    '''
    Hc = Hc/1E6
    LFL = -3.42/Hc + 0.569*Hc + 0.0538*Hc*Hc + 1.80
    return LFL/100.