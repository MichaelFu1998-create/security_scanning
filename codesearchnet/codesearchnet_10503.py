def grid_pixels_1d_to_grid_arcsec_1d(grid_pixels_1d, shape, pixel_scales, origin=(0.0, 0.0)):
    """ Convert a grid of (y,x) pixel coordinates to a grid of (y,x) arc second values.

    The pixel coordinate origin is at the top left corner of the grid, such that the pixel [0,0] corresponds to \
    higher y arc-second coordinate value and lowest x arc-second coordinate.

    The arc-second coordinate origin is defined by the class attribute origin, and coordinates are shifted to this \
    origin after computing their values from the 1D grid pixel indexes.

    The input and output grids are both of shape (total_pixels, 2).

    Parameters
    ----------
    grid_pixels_1d: ndarray
        The grid of (y,x) coordinates in pixel values which is converted to arc-second coordinates.
    shape : (int, int)
        The (y,x) shape of the original 2D array the arc-second coordinates were computed on.
    pixel_scales : (float, float)
        The (y,x) arc-second to pixel scales of the original 2D array.
    origin : (float, flloat)
        The (y,x) origin of the grid, which the arc-second grid is shifted.

    Returns
    --------
    ndarray
        A grid of 1d arc-second coordinates with dimensions (total_pixels, 2).

    Examples
    --------
    grid_pixels_1d = np.array([[0,0], [0,1], [1,0], [1,1])
    grid_pixels_1d = grid_pixels_1d_to_grid_arcsec_1d(grid_pixels_1d=grid_pixels_1d, shape=(2,2),
                                                           pixel_scales=(0.5, 0.5), origin=(0.0, 0.0))
    """

    grid_arcsec_1d = np.zeros((grid_pixels_1d.shape[0], 2))

    centres_arcsec = centres_from_shape_pixel_scales_and_origin(shape=shape, pixel_scales=pixel_scales, origin=origin)

    for i in range(grid_arcsec_1d.shape[0]):

        grid_arcsec_1d[i, 0] = -(grid_pixels_1d[i, 0] - centres_arcsec[0] - 0.5) * pixel_scales[0]
        grid_arcsec_1d[i, 1] = (grid_pixels_1d[i, 1] - centres_arcsec[1] - 0.5) * pixel_scales[1]

    return grid_arcsec_1d