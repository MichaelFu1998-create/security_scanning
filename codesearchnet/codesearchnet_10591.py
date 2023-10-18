def map_unmasked_1d_array_to_2d_array_from_array_1d_and_shape(array_1d, shape):
    """For a 1D array that was flattened from a 2D array of shape (rows, columns), map its values back to the \
    original 2D array.

    The pixel coordinate origin is at the top left corner of the 2D array and goes right-wards and downwards, such
    that for an array of shape (3,3):

    - pixel 0 of the 1D array will correspond to index [0,0] of the 2D array.
    - pixel 1 of the 1D array will correspond to index [0,1] of the 2D array.
    - pixel 4 of the 1D array will correspond to index [1,0] of the 2D array.

    Parameters
     ----------
    array_1d : ndarray
        The 1D array of values which are mapped to a 2D array.
    shape : (int, int)
        The shape of the 2D array which the pixels are defined on.

    Returns
    --------
    ndarray
        A 2D array of values mapped from the 1D array with dimensions (shape).

    Examples
    --------
    one_to_two = np.array([[0,1], [1,0], [1,1], [1,2], [2,1]])

    array_1d = np.array([[2.0, 4.0, 5.0, 6.0, 8.0])

    array_2d = map_masked_1d_array_to_2d_array_from_array_1d_shape_and_one_to_two(array_1d=array_1d, shape=(3,3),
                                                                                  one_to_two=one_to_two)
    """

    array_2d = np.zeros(shape)

    index = 0
    for y in range(shape[0]):
        for x in range(shape[1]):
            array_2d[y, x] = array_1d[index]
            index += 1

    return array_2d