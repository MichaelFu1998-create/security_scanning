def Hfus(T=298.15, P=101325, MW=None, AvailableMethods=False, Method=None, CASRN=''):  # pragma: no cover
    '''This function handles the calculation of a chemical's enthalpy of fusion.
    Generally this, is used by the chemical class, as all parameters are passed.
    Calling the function directly works okay.

    Enthalpy of fusion is a weak function of pressure, and its effects are
    neglected.

    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.

    '''
    def list_methods():
        methods = []
        if CASRN in CRCHfus_data.index:
            methods.append('CRC, at melting point')
        methods.append('None')
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    # This is the calculate, given the method section
    if Method == 'CRC, at melting point':
        _Hfus = CRCHfus_data.at[CASRN, 'Hfus']
    elif Method == 'None' or not MW:
        _Hfus = None
    else:
        raise Exception('Failure in in function')
    _Hfus = property_molar_to_mass(_Hfus, MW)
    return _Hfus