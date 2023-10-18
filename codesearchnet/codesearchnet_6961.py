def STEL(CASRN, AvailableMethods=False, Method=None):  # pragma: no cover
    '''This function handles the retrieval of Short-term Exposure Limit on
    worker exposure to dangerous chemicals.

    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.

    >>> STEL('67-64-1')
    (750.0, 'ppm')
    >>> STEL('7664-38-2')
    (0.7489774978301237, 'ppm')
    >>> STEL('55720-99-5')
    (2.0, 'mg/m^3')
    >>> STEL('86290-81-5', AvailableMethods=True)
    ['Ontario Limits', 'None']
    '''
    def list_methods():
        methods = []
        if CASRN in _OntarioExposureLimits and (_OntarioExposureLimits[CASRN]["STEL (ppm)"] or _OntarioExposureLimits[CASRN]["STEL (mg/m^3)"]):
            methods.append(ONTARIO)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == ONTARIO:
        if _OntarioExposureLimits[CASRN]["STEL (ppm)"]:
            _STEL = (_OntarioExposureLimits[CASRN]["STEL (ppm)"], 'ppm')
        elif _OntarioExposureLimits[CASRN]["STEL (mg/m^3)"]:
            _STEL = (_OntarioExposureLimits[CASRN]["STEL (mg/m^3)"], 'mg/m^3')
    elif Method == NONE:
        _STEL = None
    else:
        raise Exception('Failure in in function')
    return _STEL