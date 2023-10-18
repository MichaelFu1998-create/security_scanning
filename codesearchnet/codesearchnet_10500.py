def sub_grid_1d_masked_from_mask_pixel_scales_and_sub_grid_size(mask, pixel_scales, sub_grid_size, origin=(0.0, 0.0)):
    """ For the sub-grid, every unmasked pixel of a 2D mask array of shape (rows, columns) is divided into a finer \
    uniform grid of shape (sub_grid_size, sub_grid_size). This routine computes the (y,x) arc second coordinates at \
    the centre of every sub-pixel defined by this grid.

    Coordinates are defined from the top-left corner, where the first unmasked sub-pixel corresponds to index 0. \
    Sub-pixels that are part of the same mask array pixel are indexed next to one another, such that the second \
    sub-pixel in the first pixel has index 1, its next sub-pixel has index 2, and so forth.

    The sub-grid is returned on an array of shape (total_unmasked_pixels*sub_grid_size**2, 2). y coordinates are \
    stored in the 0 index of the second dimension, x coordinates in the 1 index.

    Parameters
     ----------
    mask : ndarray
        A 2D array of bools, where *False* values mean unmasked and are therefore included as part of the calculated \
        regular grid.
    pixel_scales : (float, float)
        The (y,x) arc-second to pixel scales of the 2D mask array.
    sub_grid_size : int
        The size of the sub-grid that each pixel of the 2D mask array is divided into.
    origin : (float, flloat)
        The (y,x) origin of the 2D array, which the sub-grid is shifted around.

    Returns
    --------
    ndarray
        A sub grid of (y,x) arc-second coordinates at the centre of every pixel unmasked pixel on the 2D mask \
        array. The sub grid array has dimensions (total_unmasked_pixels*sub_grid_size**2, 2).

    Examples
    --------
    mask = np.array([[True, False, True],
                     [False, False, False]
                     [True, False, True]])
    sub_grid_1d = sub_grid_1d_from_mask_pixel_scales_and_origin(mask=mask, pixel_scales=(0.5, 0.5), origin=(0.0, 0.0))
    """

    total_sub_pixels = mask_util.total_sub_pixels_from_mask_and_sub_grid_size(mask, sub_grid_size)

    sub_grid_1d = np.zeros(shape=(total_sub_pixels, 2))

    centres_arcsec = centres_from_shape_pixel_scales_and_origin(shape=mask.shape, pixel_scales=pixel_scales,
                                                                origin=origin)

    sub_index = 0

    y_sub_half = pixel_scales[0] / 2
    y_sub_step = pixel_scales[0] / (sub_grid_size + 1)

    x_sub_half = pixel_scales[1] / 2
    x_sub_step = pixel_scales[1] / (sub_grid_size + 1)

    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):

            if not mask[y, x]:

                y_arcsec = (y - centres_arcsec[0]) * pixel_scales[0]
                x_arcsec = (x - centres_arcsec[1]) * pixel_scales[1]

                for y1 in range(sub_grid_size):
                    for x1 in range(sub_grid_size):

                        sub_grid_1d[sub_index, 0] = -(y_arcsec - y_sub_half + (y1 + 1) * y_sub_step)
                        sub_grid_1d[sub_index, 1] = x_arcsec - x_sub_half + (x1 + 1) * x_sub_step
                        sub_index += 1

    return sub_grid_1d