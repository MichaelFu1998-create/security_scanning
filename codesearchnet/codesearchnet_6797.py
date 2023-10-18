def Hsub(T=298.15, P=101325, MW=None, AvailableMethods=False, Method=None, CASRN=''):  # pragma: no cover
    '''This function handles the calculation of a chemical's enthalpy of sublimation.
    Generally this, is used by the chemical class, as all parameters are passed.


    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.
    '''
    def list_methods():
        methods = []
#        if Hfus(T=T, P=P, MW=MW, CASRN=CASRN) and Hvap(T=T, P=P, MW=MW, CASRN=CASRN):
#            methods.append('Hfus + Hvap')
        if CASRN in GharagheiziHsub_data.index:
            methods.append('Ghazerati Appendix, at 298K')
        methods.append('None')
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    # This is the calculate, given the method section
#    if Method == 'Hfus + Hvap':
#        p1 = Hfus(T=T, P=P, MW=MW, CASRN=CASRN)
#        p2 = Hvap(T=T, P=P, MW=MW, CASRN=CASRN)
#        if p1 and p2:
#            _Hsub = p1 + p2
#        else:
#            _Hsub = None
    if Method == 'Ghazerati Appendix, at 298K':
        _Hsub = float(GharagheiziHsub_data.at[CASRN, 'Hsub'])
    elif Method == 'None' or not _Hsub or not MW:
        return None
    else:
        raise Exception('Failure in in function')
    _Hsub = property_molar_to_mass(_Hsub, MW)
    return _Hsub