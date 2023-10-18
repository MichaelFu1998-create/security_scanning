def regular_grid_1d_masked_from_mask_pixel_scales_and_origin(mask, pixel_scales, origin=(0.0, 0.0)):
    """Compute the (y,x) arc second coordinates at the centre of every pixel of a 2D mask array of shape (rows, columns).

    Coordinates are defined from the top-left corner, where the first unmasked pixel corresponds to index 0. The pixel \
    at the top-left of the array has negative x and y values in arc seconds.

    The regular grid is returned on an array of shape (total_unmasked_pixels, 2). y coordinates are stored in the 0 \
    index of the second dimension, x coordinates in the 1 index.

    Parameters
     ----------
    mask : ndarray
        A 2D array of bools, where *False* values mean unmasked and are therefore included as part of the calculated \
        regular grid.
    pixel_scales : (float, float)
        The (y,x) arc-second to pixel scales of the 2D mask array.
    origin : (float, flloat)
        The (y,x) origin of the 2D array, which the regular grid is shifted around.

    Returns
    --------
    ndarray
        A regular grid of (y,x) arc-second coordinates at the centre of every pixel unmasked pixel on the 2D mask \
        array. The regular grid array has dimensions (total_unmasked_pixels, 2).

    Examples
    --------
    mask = np.array([[True, False, True],
                     [False, False, False]
                     [True, False, True]])
    regular_grid_1d = regular_grid_1d_masked_from_mask_pixel_scales_and_origin(mask=mask, pixel_scales=(0.5, 0.5),
                                                                            origin=(0.0, 0.0))
    """

    grid_2d = regular_grid_2d_from_shape_pixel_scales_and_origin(mask.shape, pixel_scales, origin)

    total_regular_pixels = mask_util.total_regular_pixels_from_mask(mask)
    regular_grid_1d = np.zeros(shape=(total_regular_pixels, 2))
    pixel_count = 0

    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if not mask[y, x]:
                regular_grid_1d[pixel_count, :] = grid_2d[y, x]
                pixel_count += 1

    return regular_grid_1d