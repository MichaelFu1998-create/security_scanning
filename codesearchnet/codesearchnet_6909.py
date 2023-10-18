def mixture_from_any(ID):
    '''Looks up a string which may represent a mixture in the database of 
    thermo to determine the key by which the composition of that mixture can
    be obtained in the dictionary `_MixtureDict`.

    Parameters
    ----------
    ID : str
        A string or 1-element list containing the name which may represent a
        mixture.

    Returns
    -------
    key : str
        Key for access to the data on the mixture in `_MixtureDict`.

    Notes
    -----
    White space, '-', and upper case letters are removed in the search.

    Examples
    --------
    >>> mixture_from_any('R512A')
    'R512A'
    >>> mixture_from_any([u'air'])
    'Air'
    '''
    if type(ID) == list:
        if len(ID) == 1:
            ID = ID[0]
        else:
            raise Exception('If the input is a list, the list must contain only one item.')
    ID = ID.lower().strip()
    ID2 = ID.replace(' ', '')
    ID3 = ID.replace('-', '')
    for i in [ID, ID2, ID3]:
        if i in _MixtureDictLookup:
            return _MixtureDictLookup[i]
    raise Exception('Mixture name not recognized')