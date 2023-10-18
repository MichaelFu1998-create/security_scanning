def CAS_from_any(ID, autoload=False):
    '''Looks up the CAS number of a chemical by searching and testing for the
    string being any of the following types of chemical identifiers:
    
    * Name, in IUPAC form or common form or a synonym registered in PubChem
    * InChI name, prefixed by 'InChI=1S/' or 'InChI=1/'
    * InChI key, prefixed by 'InChIKey='
    * PubChem CID, prefixed by 'PubChem='
    * SMILES (prefix with 'SMILES=' to ensure smiles parsing; ex.
      'C' will return Carbon as it is an element whereas the SMILES 
      interpretation for 'C' is methane)
    * CAS number (obsolete numbers may point to the current number)    

    If the input is an ID representing an element, the following additional 
    inputs may be specified as 
    
    * Atomic symbol (ex 'Na')
    * Atomic number (as a string)

    Parameters
    ----------
    ID : str
        One of the name formats described above

    Returns
    -------
    CASRN : string
        A three-piece, dash-separated set of numbers

    Notes
    -----
    An exception is raised if the name cannot be identified. The PubChem 
    database includes a wide variety of other synonyms, but these may not be
    present for all chemcials.

    Examples
    --------
    >>> CAS_from_any('water')
    '7732-18-5'
    >>> CAS_from_any('InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3')
    '64-17-5'
    >>> CAS_from_any('CCCCCCCCCC')
    '124-18-5'
    >>> CAS_from_any('InChIKey=LFQSCWFLJHTTHZ-UHFFFAOYSA-N')
    '64-17-5'
    >>> CAS_from_any('pubchem=702')
    '64-17-5'
    >>> CAS_from_any('O') # only elements can be specified by symbol
    '17778-80-2'
    '''
    ID = ID.strip()
    ID_lower = ID.lower()
    if ID in periodic_table:
        if periodic_table[ID].number not in homonuclear_elemental_gases:
            return periodic_table[ID].CAS
        else:
            for i in [periodic_table.symbol_to_elements, 
                      periodic_table.number_to_elements,
                      periodic_table.CAS_to_elements]:
                if i == periodic_table.number_to_elements:
                    if int(ID in i):
                        return periodic_table[int(ID)].CAS
                    
                else:
                    if ID in i:
                        return periodic_table[ID].CAS

    if checkCAS(ID):
        CAS_lookup = pubchem_db.search_CAS(ID, autoload)
        if CAS_lookup:
            return CAS_lookup.CASs
        
        # handle the case of synonyms
        CAS_alternate_loopup = pubchem_db.search_name(ID, autoload)
        if CAS_alternate_loopup:
            return CAS_alternate_loopup.CASs
        if not autoload:
            return CAS_from_any(ID, autoload=True)
        raise Exception('A valid CAS number was recognized, but is not in the database')
        
        
    
    ID_len = len(ID)
    if ID_len > 9:
        inchi_search = False
        # normal upper case is 'InChI=1S/'
        if ID_lower[0:9] == 'inchi=1s/':
            inchi_search = ID[9:]
        elif ID_lower[0:8] == 'inchi=1/':
            inchi_search = ID[8:]
        if inchi_search:
            inchi_lookup = pubchem_db.search_InChI(inchi_search, autoload)
            if inchi_lookup:
                return inchi_lookup.CASs
            else:
                if not autoload:
                    return CAS_from_any(ID, autoload=True)
                raise Exception('A valid InChI name was recognized, but it is not in the database')
        if ID_lower[0:9] == 'inchikey=':
            inchi_key_lookup = pubchem_db.search_InChI_key(ID[9:], autoload)
            if inchi_key_lookup:
                return inchi_key_lookup.CASs
            else:
                if not autoload:
                    return CAS_from_any(ID, autoload=True)
                raise Exception('A valid InChI Key was recognized, but it is not in the database')
    if ID_len > 8:
        if ID_lower[0:8] == 'pubchem=':
            pubchem_lookup = pubchem_db.search_pubchem(ID[8:], autoload)
            if pubchem_lookup:
                return pubchem_lookup.CASs
            else:
                if not autoload:
                    return CAS_from_any(ID, autoload=True)
                raise Exception('A PubChem integer identifier was recognized, but it is not in the database.')
    if ID_len > 7:
        if ID_lower[0:7] == 'smiles=':
            smiles_lookup = pubchem_db.search_smiles(ID[7:], autoload)
            if smiles_lookup:
                return smiles_lookup.CASs
            else:
                if not autoload:
                    return CAS_from_any(ID, autoload=True)
                raise Exception('A SMILES identifier was recognized, but it is not in the database.')

    # Try the smiles lookup anyway
    # Parsing SMILES is an option, but this is faster
    # Pybel API also prints messages to console on failure
    smiles_lookup = pubchem_db.search_smiles(ID, autoload)
    if smiles_lookup:
        return smiles_lookup.CASs
    
    try:
        formula_query = pubchem_db.search_formula(serialize_formula(ID), autoload)
        if formula_query and type(formula_query) == ChemicalMetadata:
            return formula_query.CASs
    except:
        pass
    
    # Try a direct lookup with the name - the fastest
    name_lookup = pubchem_db.search_name(ID, autoload)
    if name_lookup:
        return name_lookup.CASs

#     Permutate through various name options
    ID_no_space = ID.replace(' ', '')
    ID_no_space_dash = ID_no_space.replace('-', '')
    
    for name in [ID, ID_no_space, ID_no_space_dash]:
        for name2 in [name, name.lower()]:
            name_lookup = pubchem_db.search_name(name2, autoload)
            if name_lookup:
                return name_lookup.CASs
            
    
    if ID[-1] == ')' and '(' in ID:#
        # Try to matck in the form 'water (H2O)'
        first_identifier, second_identifier = ID[0:-1].split('(', 1)
        try:
            CAS1 = CAS_from_any(first_identifier)
            CAS2 = CAS_from_any(second_identifier)
            assert CAS1 == CAS2
            return CAS1
        except:
            pass
        
    if not autoload:
        return CAS_from_any(ID, autoload=True)
            
    raise Exception('Chemical name not recognized')