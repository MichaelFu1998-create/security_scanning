def smarts_fragment(catalog, rdkitmol=None, smi=None):
    r'''Fragments a molecule into a set of unique groups and counts as
    specified by the `catalog`. The molecule can either be an rdkit 
    molecule object, or a smiles string which will be parsed by rdkit.
    Returns a dictionary of groups and their counts according to the
    indexes of the catalog provided.
    
    Parameters
    ----------
    catalog : dict
        Dictionary indexed by keys pointing to smarts strings, [-] 
    rdkitmol : mol, optional
        Molecule as rdkit object, [-]
    smi : str, optional
        Smiles string representing a chemical, [-]

    Returns
    -------
    counts : dict
        Dictionaty of integer counts of the found groups only, indexed by
        the same keys used by the catalog [-]
    success : bool
        Whether or not molecule was fully and uniquely fragmented, [-]
    status : str
        A string holding an explanation of why the molecule failed to be
        fragmented, if it fails; 'OK' if it suceeds.
        
    Notes
    -----
    Raises an exception if rdkit is not installed, or `smi` or `rdkitmol` is
    not defined.
        
    Examples
    --------
    Acetone:
    
    >>> smarts_fragment(catalog=J_BIGGS_JOBACK_SMARTS_id_dict, smi='CC(=O)C')
    ({24: 1, 1: 2}, True, 'OK')
    
    Sodium sulfate, (Na2O4S):
    
    >>> smarts_fragment(catalog=J_BIGGS_JOBACK_SMARTS_id_dict, smi='[O-]S(=O)(=O)[O-].[Na+].[Na+]')
    ({29: 4}, False, 'Did not match all atoms present')
    
    Propionic anhydride (C6H10O3):
        
    >>> smarts_fragment(catalog=J_BIGGS_JOBACK_SMARTS_id_dict, smi='CCC(=O)OC(=O)CC')
    ({1: 2, 2: 2, 28: 2}, False, 'Matched some atoms repeatedly: [4]')
    '''
    if not hasRDKit: # pragma: no cover
        raise Exception(rdkit_missing)
    if rdkitmol is None and smi is None:
        raise Exception('Either an rdkit mol or a smiles string is required')
    if smi is not None:
        rdkitmol = Chem.MolFromSmiles(smi)
        if rdkitmol is None:
            status = 'Failed to construct mol'
            success = False
            return {}, success, status

    atom_count = len(rdkitmol.GetAtoms())    
    status = 'OK'
    success = True
    
    counts = {}
    all_matches = {}
    for key, smart in catalog.items():
        patt = Chem.MolFromSmarts(smart)
        hits = rdkitmol.GetSubstructMatches(patt)
        if hits:
            all_matches[smart] = hits
            counts[key] = len(hits)
    
    matched_atoms = set()
    for i in all_matches.values():
        for j in i:
            matched_atoms.update(j)
    if len(matched_atoms) != atom_count:
        status = 'Did not match all atoms present'
        success = False
        
    # Check the atom aount again, this time looking for duplicate matches (only if have yet to fail)
    if success:
        matched_atoms = []
        for i in all_matches.values():
            for j in i:
                matched_atoms.extend(j)
        if len(matched_atoms) < atom_count:
            status = 'Matched %d of %d atoms only' %(len(matched_atoms), atom_count)
            success = False
        elif len(matched_atoms) > atom_count:
            status = 'Matched some atoms repeatedly: %s' %( [i for i, c in Counter(matched_atoms).items() if c > 1])
            success = False
        
    return counts, success, status