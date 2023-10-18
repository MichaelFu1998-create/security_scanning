def Ceiling(CASRN, AvailableMethods=False, Method=None):  # pragma: no cover
    '''This function handles the retrieval of Ceiling limits on worker
    exposure to dangerous chemicals.

    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.

    >>> Ceiling('75-07-0')
    (25.0, 'ppm')
    >>> Ceiling('1395-21-7')
    (6e-05, 'mg/m^3')
    >>> Ceiling('7572-29-4', AvailableMethods=True)
    ['Ontario Limits', 'None']
    '''
    def list_methods():
        methods = []
        if CASRN in _OntarioExposureLimits and (_OntarioExposureLimits[CASRN]["Ceiling (ppm)"] or _OntarioExposureLimits[CASRN]["Ceiling (mg/m^3)"]):
            methods.append(ONTARIO)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == ONTARIO:
        if _OntarioExposureLimits[CASRN]["Ceiling (ppm)"]:
            _Ceiling = (_OntarioExposureLimits[CASRN]["Ceiling (ppm)"], 'ppm')
        elif _OntarioExposureLimits[CASRN]["Ceiling (mg/m^3)"]:
            _Ceiling = (_OntarioExposureLimits[CASRN]["Ceiling (mg/m^3)"], 'mg/m^3')
    elif Method == NONE:
        _Ceiling = None
    else:
        raise Exception('Failure in in function')
    return _Ceiling