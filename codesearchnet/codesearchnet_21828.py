def dstack(tup):
    """Stack arrays in sequence depth wise (along third dimension), 
    handling ``RemoteArray`` and ``DistArray`` without moving data.

    Args:
      tup (sequence of array_like)

    Returns: 
      res: `ndarray`, if inputs were all local
           `RemoteArray`, if inputs were all on the same remote engine
           `DistArray`, if inputs were already scattered on different engines
    """
    # Follow numpy.dstack behavior for 1D and 2D arrays:
    arrays = list(tup)
    for i in range(len(arrays)):
        if arrays[i].ndim is 1:
            arrays[i] = arrays[i][np.newaxis, :]
        if arrays[i].ndim is 2:
            arrays[i] = arrays[i][:, :, np.newaxis]
    return concatenate(arrays, axis=2)