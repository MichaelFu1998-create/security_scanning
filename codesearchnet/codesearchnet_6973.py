def Crowl_Louvar_UFL(atoms):
    r'''Calculates upper flammability limit, using the Crowl-Louvar [1]_
    correlation. Uses molecular formula only.

    The upper flammability limit of a gas is air is:

    .. math::
        C_mH_xO_y + zO_2 \to mCO_2 + \frac{x}{2}H_2O

        \text{UFL} = \frac{3.5}{4.76m + 1.19x - 2.38y + 1}

    Parameters
    ----------
    atoms : dict
        Dictionary of atoms and atom counts

    Returns
    -------
    UFL : float
        Upper flammability limit, mole fraction

    Notes
    -----
    Coefficient of 3.5 taken from [2]_

    Examples
    --------
    Hexane, example from [1]_, lit. 7.5 %

    >>> Crowl_Louvar_UFL({'H': 14, 'C': 6})
    0.07572479446127219

    References
    ----------
    .. [1] Crowl, Daniel A., and Joseph F. Louvar. Chemical Process Safety:
       Fundamentals with Applications. 2E. Upper Saddle River, N.J:
       Prentice Hall, 2001.
    .. [2] Jones, G. W. "Inflammation Limits and Their Practical Application
       in Hazardous Industrial Operations." Chemical Reviews 22, no. 1
       (February 1, 1938): 1-26. doi:10.1021/cr60071a001
    '''
    nC, nH, nO = 0, 0, 0
    if 'C' in atoms and atoms['C']:
        nC = atoms['C']
    else:
        return None
    if 'H' in atoms:
        nH = atoms['H']
    if 'O' in atoms:
        nO = atoms['O']
    return 3.5/(4.76*nC + 1.19*nH - 2.38*nO + 1.)