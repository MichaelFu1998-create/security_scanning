def ndmeshgrid(*arrs):
    """Return a mesh grid for N dimensions.

    The input are N arrays, each of which contains the values along one axis of
    the coordinate system. The arrays do not have to have the same number of
    entries. The function returns arrays that can be fed into numpy functions
    so that they produce values for *all* points spanned by the axes *arrs*.

    Original from
    http://stackoverflow.com/questions/1827489/numpy-meshgrid-in-3d and fixed.

    .. SeeAlso: :func:`numpy.meshgrid` for the 2D case.
    """
    #arrs = tuple(reversed(arrs)) <-- wrong on stackoverflow.com
    arrs = tuple(arrs)
    lens = list(map(len, arrs))
    dim = len(arrs)

    sz = 1
    for s in lens:
        sz *= s

    ans = []
    for i, arr in enumerate(arrs):
        slc = [1] * dim
        slc[i] = lens[i]
        arr2 = numpy.asanyarray(arr).reshape(slc)
        for j, sz in enumerate(lens):
            if j != i:
                arr2 = arr2.repeat(sz, axis=j)
        ans.append(arr2)

    return tuple(ans)