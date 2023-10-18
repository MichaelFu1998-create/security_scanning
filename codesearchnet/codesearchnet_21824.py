def expand_dims(a, axis):
    """Insert a new axis, corresponding to a given position in the array shape

    Args:
      a (array_like): Input array.
      axis (int): Position (amongst axes) where new axis is to be inserted.
    """
    if hasattr(a, 'expand_dims') and hasattr(type(a), '__array_interface__'):
        return a.expand_dims(axis)
    else:
        return np.expand_dims(a, axis)