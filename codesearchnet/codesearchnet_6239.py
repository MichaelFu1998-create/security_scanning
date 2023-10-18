def shared_np_array(shape, data=None, integer=False):
    """Create a new numpy array that resides in shared memory.

    Parameters
    ----------
    shape : tuple of ints
        The shape of the new array.
    data : numpy.array
        Data to copy to the new array. Has to have the same shape.
    integer : boolean
        Whether to use an integer array. Defaults to False which means
        float array.

    """

    size = np.prod(shape)

    if integer:
        array = Array(ctypes.c_int64, int(size))
        np_array = np.frombuffer(array.get_obj(), dtype="int64")
    else:
        array = Array(ctypes.c_double, int(size))
        np_array = np.frombuffer(array.get_obj())

    np_array = np_array.reshape(shape)

    if data is not None:
        if len(shape) != len(data.shape):
            raise ValueError("`data` must have the same dimensions"
                             "as the created array.")
        same = all(x == y for x, y in zip(shape, data.shape))

        if not same:
            raise ValueError("`data` must have the same shape"
                             "as the created array.")
        np_array[:] = data

    return np_array