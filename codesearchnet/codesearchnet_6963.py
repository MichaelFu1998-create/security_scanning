def Skin(CASRN, AvailableMethods=False, Method=None):  # pragma: no cover
    '''This function handles the retrieval of whether or not a chemical can
    be absorbed through the skin, relevant to chemical safety calculations.

    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.

    >>> Skin('108-94-1')
    True
    >>> Skin('1395-21-7')
    False
    >>> Skin('7572-29-4', AvailableMethods=True)
    ['Ontario Limits', 'None']
    '''
    def list_methods():
        methods = []
        if CASRN in _OntarioExposureLimits:
            methods.append(ONTARIO)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == ONTARIO:
        _Skin = (_OntarioExposureLimits[CASRN]["Skin"])
    elif Method == NONE:
        _Skin = None
    else:
        raise Exception('Failure in in function')
    return _Skin