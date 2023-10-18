def economic_status(CASRN, Method=None, AvailableMethods=False):  # pragma: no cover
    '''Look up the economic status of a chemical.

    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.

    >>> pprint(economic_status(CASRN='98-00-0'))
    ["US public: {'Manufactured': 0.0, 'Imported': 10272.711, 'Exported': 184.127}",
     u'10,000 - 100,000 tonnes per annum',
     'OECD HPV Chemicals']

    >>> economic_status(CASRN='13775-50-3')  # SODIUM SESQUISULPHATE
    []
    >>> economic_status(CASRN='98-00-0', Method='OECD high production volume chemicals')
    'OECD HPV Chemicals'
    >>> economic_status(CASRN='98-01-1', Method='European Chemicals Agency Total Tonnage Bands')
    [u'10,000 - 100,000 tonnes per annum']
    '''
    load_economic_data()
    CASi = CAS2int(CASRN)

    def list_methods():
        methods = []
        methods.append('Combined')
        if CASRN in _EPACDRDict:
            methods.append(EPACDR)
        if CASRN in _ECHATonnageDict:
            methods.append(ECHA)
        if CASi in HPV_data.index:
            methods.append(OECD)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    # This is the calculate, given the method section
    if Method == EPACDR:
        status = 'US public: ' + str(_EPACDRDict[CASRN])
    elif Method == ECHA:
        status = _ECHATonnageDict[CASRN]
    elif Method == OECD:
        status = 'OECD HPV Chemicals'
    elif Method == 'Combined':
        status = []
        if CASRN in _EPACDRDict:
            status += ['US public: ' + str(_EPACDRDict[CASRN])]
        if CASRN in _ECHATonnageDict:
            status += _ECHATonnageDict[CASRN]
        if CASi in HPV_data.index:
            status += ['OECD HPV Chemicals']
    elif Method == NONE:
        status = None
    else:
        raise Exception('Failure in in function')
    return status