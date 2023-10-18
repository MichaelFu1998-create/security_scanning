def Tc_mixture(Tcs=None, zs=None, CASRNs=None, AvailableMethods=False, Method=None):  # pragma: no cover
    '''This function handles the retrival of a mixture's critical temperature.

    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.

    >>> Tc_mixture([400, 550], [0.3, 0.7])
    505.0
    '''
    def list_methods():
        methods = []
        if none_and_length_check([Tcs]):
            methods.append('Simple')
        methods.append('None')
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    # This is the calculate, given the method section
    if Method == 'Simple':
        return mixing_simple(zs, Tcs)
    elif Method == 'None':
        return None
    else:
        raise Exception('Failure in in function')