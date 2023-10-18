def UFL_mixture(ys=None, UFLs=None, CASRNs=None, AvailableMethods=False,
                Method=None):  # pragma: no cover
    '''Inert gases are ignored.

    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.

    >>> UFL_mixture(ys=normalize([0.0024, 0.0061, 0.0015]), UFLs=[.075, .15, .32])
    0.12927551844869378
    >>> LFL_mixture(LFLs=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0.143, 0.36, 0.63, 0.1097, 0.072], ys=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.10, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05], CASRNs=['7440-37-1', '124-38-9', '7440-59-7', '7440-01-9', '7727-37-9', '7440-63-3', '10102-43-9', '7782-44-7', '132259-10-0', '7439-90-9', '10043-92-2', '7732-18-5', '7782-50-5', '7782-41-4', '67-64-1', '67-56-1', '75-52-5', '590-19-2', '277-10-1'])
    0.14550641757359664
    '''
    def list_methods():
        methods = []
        if CASRNs:
            CASRNs2 = list(CASRNs)
            UFLs2 = list(UFLs)
            for i in inerts:
                if i in CASRNs2:
                    ind = CASRNs.index(i)
                    CASRNs2.remove(i)
                    UFLs2.remove(UFLs[ind])
            if none_and_length_check([UFLs2]):
                methods.append('Summed Inverse, inerts removed')
        if none_and_length_check([UFLs, ys]):
            methods.append('Summed Inverse')
        methods.append('None')
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    # This is the calculate, given the method section
#    if not none_and_length_check([UFLs, ys]):  # check same-length inputs
#        raise Exception('Function inputs are incorrect format')
    if Method == 'Summed Inverse':
        return fire_mixing(ys, UFLs)
    elif Method == 'Summed Inverse, inerts removed':
        CASRNs2 = list(CASRNs)
        UFLs2 = list(UFLs)
        ys2 = list(ys)
        for i in inerts:
            if i in CASRNs2:
                ind = CASRNs2.index(i)
                CASRNs2.remove(i)
                UFLs2.pop(ind)
                ys2.pop(ind)
        return fire_mixing(normalize(ys2), UFLs2)
    elif Method == 'None':
        return None
    else:
        raise Exception('Failure in in function')