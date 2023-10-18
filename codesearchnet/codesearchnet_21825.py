def concatenate(tup, axis=0):
    """Join a sequence of arrays together. 
    Will aim to join `ndarray`, `RemoteArray`, and `DistArray` without moving 
    their data, if they happen to be on different engines.

    Args:
      tup (sequence of array_like): Arrays to be concatenated. They must have
        the same shape, except in the dimension corresponding to `axis`.
      axis (int, optional): The axis along which the arrays will be joined.

    Returns: 
      res: `ndarray`, if inputs were all local
           `RemoteArray`, if inputs were all on the same remote engine
           `DistArray`, if inputs were already scattered on different engines
    """
    from distob import engine
    if len(tup) is 0:
        raise ValueError('need at least one array to concatenate')
    first = tup[0]
    others = tup[1:]
    # allow subclasses to provide their own implementations of concatenate:
    if (hasattr(first, 'concatenate') and 
            hasattr(type(first), '__array_interface__')):
        return first.concatenate(others, axis)
    # convert all arguments to arrays/RemoteArrays if they are not already:
    arrays = []
    for ar in tup:
        if isinstance(ar, DistArray):
            if axis == ar._distaxis:
                arrays.extend(ar._subarrays)
            else:
                # Since not yet implemented arrays distributed on more than
                # one axis, will fetch and re-scatter on the new axis:
                arrays.append(gather(ar))
        elif isinstance(ar, RemoteArray):
            arrays.append(ar)
        elif isinstance(ar, Remote):
            arrays.append(_remote_to_array(ar))
        elif hasattr(type(ar), '__array_interface__'):
            # then treat as a local ndarray
            arrays.append(ar)
        else:
            arrays.append(np.array(ar))
    if all(isinstance(ar, np.ndarray) for ar in arrays):
        return np.concatenate(arrays, axis)
    total_length = 0
    # validate dimensions are same, except for axis of concatenation:
    commonshape = list(arrays[0].shape)
    commonshape[axis] = None # ignore this axis for shape comparison
    for ar in arrays:
        total_length += ar.shape[axis]
        shp = list(ar.shape)
        shp[axis] = None
        if shp != commonshape:
            raise ValueError('incompatible shapes for concatenation')
    # set sensible target block size if splitting subarrays further:
    blocksize = ((total_length - 1) // engine.nengines) + 1
    rarrays = []
    for ar in arrays:
        if isinstance(ar, DistArray):
            rarrays.extend(ar._subarrays)
        elif isinstance(ar, RemoteArray):
            rarrays.append(ar)
        else:
            da = _scatter_ndarray(ar, axis, blocksize)
            for ra in da._subarrays:
                rarrays.append(ra)
            del da
    del arrays
    # At this point rarrays is a list of RemoteArray to be concatenated
    eid = rarrays[0]._id.engine
    if all(ra._id.engine == eid for ra in rarrays):
        # Arrays to be joined are all on the same engine
        if eid == engine.eid:
            # Arrays are all local
            return concatenate([gather(r) for r in rarrays], axis)
        else:
            return call(concatenate, rarrays, axis)
    else:
        # Arrays to be joined are on different engines.
        # TODO: consolidate any consecutive arrays already on same engine
        return DistArray(rarrays, axis)