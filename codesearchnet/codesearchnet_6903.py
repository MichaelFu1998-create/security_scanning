def Pc_mixture(Pcs=None, zs=None, CASRNs=None, AvailableMethods=False, Method=None):  # pragma: no cover
    '''This function handles the retrival of a mixture's critical temperature.

    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.

    >>> Pc_mixture([2.2E7, 1.1E7], [0.3, 0.7])
    14300000.0
    '''
    def list_methods():
        methods = []
        if none_and_length_check([Pcs]):
            methods.append('Simple')
        methods.append('None')
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    # This is the calculate, given the method section
    if Method == 'Simple':
        return mixing_simple(zs, Pcs)
    elif Method == 'None':
        return None
    else:
        raise Exception('Failure in in function')