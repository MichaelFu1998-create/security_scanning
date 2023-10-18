def molecular_weight(atoms):
    r'''Calculates molecular weight of a molecule given a dictionary of its
    atoms and their counts, in the format {symbol: count}.

    .. math::
        MW = \sum_i n_i MW_i

    Parameters
    ----------
    atoms : dict
        dictionary of counts of individual atoms, indexed by symbol with
        proper capitalization, [-]

    Returns
    -------
    MW : float
        Calculated molecular weight [g/mol]

    Notes
    -----
    Elemental data is from rdkit, with CAS numbers added. An exception is
    raised if an incorrect element symbol is given. Elements up to 118 are
    supported, as are deutreium and tritium.

    Examples
    --------
    >>> molecular_weight({'H': 12, 'C': 20, 'O': 5}) # DNA
    332.30628

    References
    ----------
    .. [1] RDKit: Open-source cheminformatics; http://www.rdkit.org
    '''
    MW = 0
    for i in atoms:
        if i in periodic_table:
            MW += periodic_table[i].MW*atoms[i]
        elif i == 'D':
            # Hardcoded MW until an actual isotope db is created
            MW += 2.014102*atoms[i]
        elif i == 'T':
            # Hardcoded MW until an actual isotope db is created
            MW += 3.0160492*atoms[i]
        else:
            raise Exception('Molecule includes unknown atoms')
    return MW