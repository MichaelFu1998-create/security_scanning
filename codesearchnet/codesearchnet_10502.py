def grid_arcsec_1d_to_grid_pixel_indexes_1d(grid_arcsec_1d, shape, pixel_scales, origin=(0.0, 0.0)):
    """ Convert a grid of (y,x) arc second coordinates to a grid of (y,x) pixel 1D indexes. Pixel coordinates are \
    returned as integers such that they are the pixel from the top-left of the 2D grid going rights and then \
    downwards.

    For example:

    The pixel at the top-left, whose 2D index is [0,0], corresponds to 1D index 0.
    The fifth pixel on the top row, whose 2D index is [0,5], corresponds to 1D index 4.
    The first pixel on the second row, whose 2D index is [0,1], has 1D index 10 if a row has 10 pixels.

    The arc-second coordinate grid is defined by the class attribute origin, and coordinates are shifted to this \
    origin before computing their 1D grid pixel indexes.

    The input and output grids are both of shape (total_pixels, 2).

    Parameters
    ----------
    grid_arcsec_1d: ndarray
        The grid of (y,x) coordinates in arc seconds which is converted to 1D pixel indexes.
    shape : (int, int)
        The (y,x) shape of the original 2D array the arc-second coordinates were computed on.
    pixel_scales : (float, float)
        The (y,x) arc-second to pixel scales of the original 2D array.
    origin : (float, flloat)
        The (y,x) origin of the grid, which the arc-second grid is shifted.

    Returns
    --------
    ndarray
        A grid of 1d pixel indexes with dimensions (total_pixels, 2).

    Examples
    --------
    grid_arcsec_1d = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]])
    grid_pixels_1d = grid_arcsec_1d_to_grid_pixel_indexes_1d(grid_arcsec_1d=grid_arcsec_1d, shape=(2,2),
                                                           pixel_scales=(0.5, 0.5), origin=(0.0, 0.0))
    """

    grid_pixels_1d = grid_arcsec_1d_to_grid_pixel_centres_1d(grid_arcsec_1d=grid_arcsec_1d, shape=shape,
                                                               pixel_scales=pixel_scales, origin=origin)

    grid_pixel_indexes_1d = np.zeros(grid_pixels_1d.shape[0])

    for i in range(grid_pixels_1d.shape[0]):

        grid_pixel_indexes_1d[i] = int(grid_pixels_1d[i,0] * shape[1] + grid_pixels_1d[i,1])

    return grid_pixel_indexes_1d