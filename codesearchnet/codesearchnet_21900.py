def _scatter_ndarray(ar, axis=-1, destination=None, blocksize=None):
    """Turn a numpy ndarray into a DistArray or RemoteArray
    Args:
     ar (array_like)
     axis (int, optional): specifies along which axis to split the array to 
       distribute it. The default is to split along the last axis. `None` means
       do not distribute.
     destination (int or list of int, optional): Optionally force the array to
       go to a specific engine. If an array is to be scattered along an axis, 
       this should be a list of engine ids with the same length as that axis.
     blocksize (int): Optionally control the size of intervals into which the
       distributed axis is split (the default splits the distributed axis
       evenly over all computing engines).
    """
    from .arrays import DistArray, RemoteArray
    shape = ar.shape
    ndim = len(shape)
    if axis is None:
        return _directed_scatter([ar], destination=[destination],
                                 blocksize=blocksize)[0]
    if axis < -ndim or axis > ndim - 1:
        raise DistobValueError('axis out of range')
    if axis < 0:
        axis = ndim + axis
    n = shape[axis]
    if n == 1:
        return _directed_scatter([ar], destination=[destination])[0]
    if isinstance(destination, collections.Sequence):
        ne = len(destination) # number of engines to scatter array to
    else:
        if distob.engine is None:
            setup_engines()
        ne = distob.engine.nengines # by default scatter across all engines
    if blocksize is None:
        blocksize = ((n - 1) // ne) + 1
    if blocksize > n:
        blocksize = n
    if isinstance(ar, DistArray):
        if axis == ar._distaxis:
            return ar
        else:
            raise DistobError('Currently can only scatter one axis of array')
    # Currently, if requested to scatter an array that is already Remote and
    # large, first get whole array locally, then scatter. Not really optimal.
    if isinstance(ar, RemoteArray) and n > blocksize:
        ar = ar._ob
    s = slice(None)
    subarrays = []
    low = 0
    for i in range(0, n // blocksize):
        high = low + blocksize
        index = (s,)*axis + (slice(low, high),) + (s,)*(ndim - axis - 1)
        subarrays.append(ar[index])
        low += blocksize
    if n % blocksize != 0:
        high = low + (n % blocksize)
        index = (s,)*axis + (slice(low, high),) + (s,)*(ndim - axis - 1)
        subarrays.append(ar[index])
    subarrays = _directed_scatter(subarrays, destination=destination)
    return DistArray(subarrays, axis)