def grid_arcsec_2d_to_grid_pixel_centres_2d(grid_arcsec_2d, shape, pixel_scales, origin=(0.0, 0.0)):
    """ Convert a grid of (y,x) arc second coordinates to a grid of (y,x) pixel values. Pixel coordinates are \
    returned as integers such that they map directly to the pixel they are contained within.

    The pixel coordinate origin is at the top left corner of the grid, such that the pixel [0,0] corresponds to \
    higher y arc-second coordinate value and lowest x arc-second coordinate.

    The arc-second coordinate grid is defined by the class attribute origin, and coordinates are shifted to this \
    origin before computing their 1D grid pixel indexes.

    The input and output grids are both of shape (total_pixels, 2).

    Parameters
    ----------
    grid_arcsec_1d: ndarray
        The grid of (y,x) coordinates in arc seconds which is converted to pixel indexes.
    shape : (int, int)
        The (y,x) shape of the original 2D array the arc-second coordinates were computed on.
    pixel_scales : (float, float)
        The (y,x) arc-second to pixel scales of the original 2D array.
    origin : (float, flloat)
        The (y,x) origin of the grid, which the arc-second grid is shifted

    Returns
    --------
    ndarray
        A grid of (y,x) pixel indexes with dimensions (total_pixels, 2).

    Examples
    --------
    grid_arcsec_1d = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]])
    grid_pixels_1d = grid_arcsec_1d_to_grid_pixel_centres_1d(grid_arcsec_1d=grid_arcsec_1d, shape=(2,2),
                                                           pixel_scales=(0.5, 0.5), origin=(0.0, 0.0))
    """

    grid_pixels_2d = np.zeros((grid_arcsec_2d.shape[0], grid_arcsec_2d.shape[1], 2))

    centres_arcsec = centres_from_shape_pixel_scales_and_origin(shape=shape, pixel_scales=pixel_scales, origin=origin)

    for y in range(grid_arcsec_2d.shape[0]):
        for x in range(grid_arcsec_2d.shape[1]):
            grid_pixels_2d[y, x, 0] = int((-grid_arcsec_2d[y, x, 0] / pixel_scales[0]) + centres_arcsec[0] + 0.5)
            grid_pixels_2d[y, x, 1] = int((grid_arcsec_2d[y, x, 1] / pixel_scales[1]) + centres_arcsec[1] + 0.5)

    return grid_pixels_2d