def transpose(a, axes=None):
    """Returns a view of the array with axes transposed.

    For a 1-D array, this has no effect.
    For a 2-D array, this is the usual matrix transpose.
    For an n-D array, if axes are given, their order indicates how the
    axes are permuted

    Args:
      a (array_like): Input array.
      axes (list of int, optional): By default, reverse the dimensions,
        otherwise permute the axes according to the values given.
    """
    if isinstance(a, np.ndarray):
        return np.transpose(a, axes)
    elif isinstance(a, RemoteArray):
        return a.transpose(*axes)
    elif isinstance(a, Remote):
        return _remote_to_array(a).transpose(*axes)
    elif isinstance(a, DistArray):
        if axes is None:
            axes = range(a.ndim - 1, -1, -1)
        axes = list(axes)
        if len(set(axes)) < len(axes):
            raise ValueError("repeated axis in transpose")
        if sorted(axes) != list(range(a.ndim)):
            raise ValueError("axes don't match array")
        distaxis = a._distaxis
        new_distaxis = axes.index(distaxis)
        new_subarrays = [ra.transpose(*axes) for ra in a._subarrays]
        return DistArray(new_subarrays, new_distaxis)
    else:
        return np.transpose(a, axes)