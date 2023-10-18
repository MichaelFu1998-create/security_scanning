def _calc_ilm_order(imshape):
    """
    Calculates an ilm order based on the shape of an image. This is based on
    something that works for our particular images. Your mileage will vary.

    Parameters
    ----------
        imshape : 3-element list-like
            The shape of the image.

    Returns
    -------
        npts : tuple
            The number of points to use for the ilm.
        zorder : int
            The order of the z-polynomial.
    """
    zorder = int(imshape[0] / 6.25) + 1
    l_npts = int(imshape[1] / 42.5)+1
    npts = ()
    for a in range(l_npts):
        if a < 5:
            npts += (int(imshape[2] * [59, 39, 29, 19, 14][a]/512.) + 1,)
        else:
            npts += (int(imshape[2] * 11/512.) + 1,)
    return npts, zorder