def hstack(tup):
    """Stack arrays in sequence horizontally (column wise), 
    handling ``RemoteArray`` and ``DistArray`` without moving data.

    Args:
      tup (sequence of array_like)

    Returns: 
      res: `ndarray`, if inputs were all local
           `RemoteArray`, if inputs were all on the same remote engine
           `DistArray`, if inputs were already scattered on different engines
    """
    # Follow numpy.hstack behavior for 1D arrays:
    if all(ar.ndim is 1 for ar in tup):
        return concatenate(tup, axis=0)
    else:
        return concatenate(tup, axis=1)