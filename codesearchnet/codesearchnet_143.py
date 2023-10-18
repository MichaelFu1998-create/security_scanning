def normalize_shape(shape):
    """
    Normalize a shape tuple or array to a shape tuple.

    Parameters
    ----------
    shape : tuple of int or ndarray
        The input to normalize. May optionally be an array.

    Returns
    -------
    tuple of int
        Shape tuple.

    """
    if isinstance(shape, tuple):
        return shape
    assert ia.is_np_array(shape), (
        "Expected tuple of ints or array, got %s." % (type(shape),))
    return shape.shape