def sub_to_regular_from_mask(mask, sub_grid_size):
    """"For pixels on a 2D array of shape (rows, colums), compute a 1D array which, for every unmasked pixel on
    this 2D array, maps the 1D sub-pixel indexes to their 1D pixel indexes.

    For example, the following mappings from sub-pixels to 2D array pixels are:

    - sub_to_regular[0] = 0 -> The first sub-pixel maps to the first unmasked pixel on the regular 2D array.
    - sub_to_regular[3] = 0 -> The fourth sub-pixel maps to the first unmaksed pixel on the regular 2D array.
    - sub_to_regular[7] = 1 -> The eighth sub-pixel maps to the second unmasked pixel on the regular 2D array.

    The term 'regular' is used because the regular-grid is defined as the grid of coordinates on the centre of every \
    pixel on the 2D array. Thus, this array maps sub-pixels on a sub-grid to regular-pixels on a regular-grid.

    Parameters
     ----------
    mask : ndarray
        A 2D array of bools, where *False* values mean unmasked and are therefore included as part of the sub-grid 2D \
        array's regular grid and sub-grid.
    sub_grid_size : int
        The size of the sub-grid that each pixel of the 2D array is divided into.

    Returns
    --------
    ndarray
        An array of integers which maps every sub-pixel index to regular-pixel index with dimensions
        (total_unmasked_pixels*sub_grid_size**2).

    Examples
    --------
    mask = np.array([[True, False, True],
                     [False, False, False]
                     [True, False, True]])
    sub_to_regular = sub_to_regular_from_mask(mask=mask, sub_grid_size=2)
    """

    total_sub_pixels = mask_util.total_sub_pixels_from_mask_and_sub_grid_size(mask=mask, sub_grid_size=sub_grid_size)

    sub_to_regular = np.zeros(shape=total_sub_pixels)
    regular_index = 0
    sub_index = 0

    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if not mask[y, x]:
                for y1 in range(sub_grid_size):
                    for x1 in range(sub_grid_size):
                        sub_to_regular[sub_index] = regular_index
                        sub_index += 1

                regular_index += 1

    return sub_to_regular