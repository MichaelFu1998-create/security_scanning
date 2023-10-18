def rollaxis(a, axis, start=0):
    """Roll the specified axis backwards, until it lies in a given position.

    Args:
      a (array_like): Input array.
      axis (int): The axis to roll backwards.  The positions of the other axes 
        do not change relative to one another.
      start (int, optional): The axis is rolled until it lies before this 
        position.  The default, 0, results in a "complete" roll.

    Returns:
      res (ndarray)
    """
    if isinstance(a, np.ndarray):
        return np.rollaxis(a, axis, start)
    if axis not in range(a.ndim):
        raise ValueError(
                'rollaxis: axis (%d) must be >=0 and < %d' % (axis, a.ndim))
    if start not in range(a.ndim + 1):
        raise ValueError(
                'rollaxis: start (%d) must be >=0 and < %d' % (axis, a.ndim+1))
    axes = list(range(a.ndim))
    axes.remove(axis)
    axes.insert(start, axis)
    return transpose(a, axes)