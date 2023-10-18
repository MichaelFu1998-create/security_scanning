def regular_grid_1d_from_shape_pixel_scales_and_origin(shape, pixel_scales, origin=(0.0, 0.0)):
    """Compute the (y,x) arc second coordinates at the centre of every pixel of an array of shape (rows, columns).

    Coordinates are defined from the top-left corner, such that the first pixel at location [0, 0] has negative x \
    and y values in arc seconds.

    The regular grid is returned on an array of shape (total_pixels**2, 2) where the 2D dimension of the original 2D \
    array are reduced to one dimension. y coordinates are stored in the 0 index of the second dimension, x coordinates
    in the 1 index.

    Parameters
     ----------
    shape : (int, int)
        The (y,x) shape of the 2D array the regular grid of coordinates is computed for.
    pixel_scales : (float, float)
        The (y,x) arc-second to pixel scales of the 2D array.
    origin : (float, flloat)
        The (y,x) origin of the 2D array, which the regular grid is shifted around.

    Returns
    --------
    ndarray
        A regular grid of (y,x) arc-second coordinates at the centre of every pixel on a 2D array. The regular grid
        array has dimensions (total_pixels**2, 2).

    Examples
    --------
    regular_grid_1d = regular_grid_1d_from_shape_pixel_scales_and_origin(shape=(5,5), pixel_scales=(0.5, 0.5), \
                                                                      origin=(0.0, 0.0))
    """

    regular_grid_1d = np.zeros((shape[0]*shape[1], 2))

    centres_arcsec = centres_from_shape_pixel_scales_and_origin(shape=shape, pixel_scales=pixel_scales, origin=origin)

    i=0
    for y in range(shape[0]):
        for x in range(shape[1]):

            regular_grid_1d[i, 0] = -(y - centres_arcsec[0]) * pixel_scales[0]
            regular_grid_1d[i, 1] = (x - centres_arcsec[1]) * pixel_scales[1]
            i += 1

    return regular_grid_1d