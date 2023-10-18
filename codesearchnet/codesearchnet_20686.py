def have_same_shape(array1, array2, nd_to_check=None):
    """
    Returns true if array1 and array2 have the same shapes, false
    otherwise.

    Parameters
    ----------
    array1: numpy.ndarray

    array2: numpy.ndarray

    nd_to_check: int
        Number of the dimensions to check, i.e., if == 3 then will check only the 3 first numbers of array.shape.
    Returns
    -------
    bool
    """
    shape1 = array1.shape
    shape2 = array2.shape
    if nd_to_check is not None:
        if len(shape1) < nd_to_check:
            msg = 'Number of dimensions to check {} is out of bounds for the shape of the first image: \n{}\n.'.format(shape1)
            raise ValueError(msg)
        elif len(shape2) < nd_to_check:
            msg = 'Number of dimensions to check {} is out of bounds for the shape of the second image: \n{}\n.'.format(shape2)
            raise ValueError(msg)

        shape1 = shape1[:nd_to_check]
        shape2 = shape2[:nd_to_check]

    return shape1 == shape2