def empty_like(array, dtype=None):
    """ Create a shared memory array from the shape of array.
    """
    array = numpy.asarray(array)
    if dtype is None: 
        dtype = array.dtype
    return anonymousmemmap(array.shape, dtype)