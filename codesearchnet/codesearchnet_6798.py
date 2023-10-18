def Tliquidus(Tms=None, ws=None, xs=None, CASRNs=None, AvailableMethods=False,
              Method=None):  # pragma: no cover
    '''This function handles the retrival of a mixtures's liquidus point.

    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.

    >>> Tliquidus(Tms=[250.0, 350.0], xs=[0.5, 0.5])
    350.0
    >>> Tliquidus(Tms=[250, 350], xs=[0.5, 0.5], Method='Simple')
    300.0
    >>> Tliquidus(Tms=[250, 350], xs=[0.5, 0.5], AvailableMethods=True)
    ['Maximum', 'Simple', 'None']
    '''
    def list_methods():
        methods = []
        if none_and_length_check([Tms]):
            methods.append('Maximum')
            methods.append('Simple')
        methods.append('None')
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    # This is the calculate, given the method section
    if Method == 'Maximum':
        _Tliq = max(Tms)
    elif Method == 'Simple':
        _Tliq = mixing_simple(xs, Tms)
    elif Method == 'None':
        return None
    else:
        raise Exception('Failure in in function')
    return _Tliq