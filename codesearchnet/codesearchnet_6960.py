def TWA(CASRN, AvailableMethods=False, Method=None):  # pragma: no cover
    '''This function handles the retrieval of Time-Weighted Average limits on worker
    exposure to dangerous chemicals.

    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.

    >>> TWA('98-00-0')
    (10.0, 'ppm')
    >>> TWA('1303-00-0')
    (5.0742430905659505e-05, 'ppm')
    >>> TWA('7782-42-5', AvailableMethods=True)
    ['Ontario Limits', 'None']
    '''
    def list_methods():
        methods = []
        if CASRN in _OntarioExposureLimits and (_OntarioExposureLimits[CASRN]["TWA (ppm)"] or _OntarioExposureLimits[CASRN]["TWA (mg/m^3)"]):
            methods.append(ONTARIO)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == ONTARIO:
        if _OntarioExposureLimits[CASRN]["TWA (ppm)"]:
            _TWA = (_OntarioExposureLimits[CASRN]["TWA (ppm)"], 'ppm')
        elif _OntarioExposureLimits[CASRN]["TWA (mg/m^3)"]:
            _TWA = (_OntarioExposureLimits[CASRN]["TWA (mg/m^3)"], 'mg/m^3')
    elif Method == NONE:
        _TWA = None
    else:
        raise Exception('Failure in in function')
    return _TWA