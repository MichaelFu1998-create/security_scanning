def centres_from_shape_pixel_scales_and_origin(shape, pixel_scales, origin):
    """Determine the (y,x) arc-second central coordinates of an array from its shape, pixel-scales and origin.

     The coordinate system is defined such that the positive y axis is up and positive x axis is right.

    Parameters
     ----------
    shape : (int, int)
        The (y,x) shape of the 2D array the arc-second centre is computed for.
    pixel_scales : (float, float)
        The (y,x) arc-second to pixel scales of the 2D array.
    origin : (float, flloat)
        The (y,x) origin of the 2D array, which the centre is shifted to.

    Returns
    --------
    tuple (float, float)
        The (y,x) arc-second central coordinates of the input array.

    Examples
    --------
    centres_arcsec = centres_from_shape_pixel_scales_and_origin(shape=(5,5), pixel_scales=(0.5, 0.5), origin=(0.0, 0.0))
    """

    y_centre_arcsec = float(shape[0] - 1) / 2 + (origin[0] / pixel_scales[0])
    x_centre_arcsec = float(shape[1] - 1) / 2 - (origin[1] / pixel_scales[1])

    return (y_centre_arcsec, x_centre_arcsec)