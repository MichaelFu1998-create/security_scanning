def map_2d_array_to_masked_1d_array_from_array_2d_and_mask(mask, array_2d):
    """For a 2D array and mask, map the values of all unmasked pixels to a 1D array.

    The pixel coordinate origin is at the top left corner of the 2D array and goes right-wards and downwards, such
    that for an array of shape (3,3) where all pixels are unmasked:

    - pixel [0,0] of the 2D array will correspond to index 0 of the 1D array.
    - pixel [0,1] of the 2D array will correspond to index 1 of the 1D array.
    - pixel [1,0] of the 2D array will correspond to index 4 of the 1D array.

    Parameters
     ----------
    mask : ndarray
        A 2D array of bools, where *False* values mean unmasked and are included in the mapping.
    array_2d : ndarray
        The 2D array of values which are mapped to a 1D array.

    Returns
    --------
    ndarray
        A 1D array of values mapped from the 2D array with dimensions (total_unmasked_pixels).

    Examples
    --------
    mask = np.array([[True, False, True],
                     [False, False, False]
                     [True, False, True]])

    array_2d = np.array([[1.0, 2.0, 3.0],
                          [4.0, 5.0, 6.0],
                          [7.0, 8.0, 9.0]])

    array_1d = map_2d_array_to_masked_1d_array_from_array_2d_and_mask(mask=mask, array_2d=array_2d)
    """

    total_image_pixels = mask_util.total_regular_pixels_from_mask(mask)

    array_1d = np.zeros(shape=total_image_pixels)
    index = 0

    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if not mask[y, x]:
                array_1d[index] = array_2d[y, x]
                index += 1

    return array_1d