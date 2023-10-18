def Vc_mixture(Vcs=None, zs=None, CASRNs=None, AvailableMethods=False, Method=None):  # pragma: no cover
    '''This function handles the retrival of a mixture's critical temperature.

    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.

    >>> Vc_mixture([5.6E-5, 2E-4], [0.3, 0.7])
    0.0001568
    '''
    def list_methods():
        methods = []
        if none_and_length_check([Vcs]):
            methods.append('Simple')
        methods.append('None')
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    # This is the calculate, given the method section
    if Method == 'Simple':
        return mixing_simple(zs, Vcs)
    elif Method == 'None':
        return None
    else:
        raise Exception('Failure in in function')