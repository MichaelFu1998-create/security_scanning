def calculate_linescan_ilm_psf(y,z, polar_angle=0., nlpts=1,
        pinhole_width=1, use_laggauss=False, **kwargs):
    """
    Calculates the illumination PSF for a line-scanning confocal with the
    confocal line oriented along the x direction.

    Parameters
    ----------
        y : numpy.ndarray
            The y points (in-plane, perpendicular to the line direction)
            at which to evaluate the illumination PSF, in units of 1/k.
            Arbitrary shape.
        z : numpy.ndarray
            The z points (optical axis) at which to evaluate the illum-
            ination PSF, in units of 1/k. Must be the same shape as `y`
        polar_angle : Float, optional
            The angle of the illuminating light's polarization with
            respect to the line's orientation along x. Default is 0.
        pinhole_width : Float, optional
            The width of the geometric image of the line projected onto
            the sample, in units of 1/k. Default is 1. The perfect line
            image is assumed to be a Gaussian. If `nlpts` is set to 1,
            the line will always be of zero width.
        nlpts : Int, optional
            The number of points to use for Hermite-gauss quadrature over
            the line's width. Default is 1, corresponding to a zero-width
            line.
        use_laggauss : Bool, optional
            Set to True to use a more-accurate sinh'd Laguerre-Gauss
            quadrature for integration over the line's length (more accurate
            in the same amount of time). Default is False for backwards
            compatibility.  FIXME what did we do here?

    Other Parameters
    ----------------
        alpha : Float, optional
            The acceptance angle of the lens, on (0,pi/2). Default is 1.
        zint : Float, optional
            The distance of the len's unaberrated focal point from the
            optical interface, in units of 1/k. Default is 100.
        n2n1 : Float, optional
            The ratio n2/n1 of the index mismatch between the sample
            (index n2) and the optical train (index n1). Must be on
            [0,inf) but should be near 1. Default is 0.95

    Returns
    -------
        hilm : numpy.ndarray
            The line illumination, of the same shape as y and z.
    """
    if use_laggauss:
        x_vals, wts = calc_pts_lag()
    else:
        x_vals, wts = calc_pts_hg()

    #I'm assuming that y,z are already some sort of meshgrid
    xg, yg, zg = [np.zeros( list(y.shape) + [x_vals.size] ) for a in range(3)]
    hilm = np.zeros(xg.shape)

    for a in range(x_vals.size):
        xg[...,a] = x_vals[a]
        yg[...,a] = y.copy()
        zg[...,a] = z.copy()

    y_pinhole, wts_pinhole = np.polynomial.hermite.hermgauss(nlpts)
    y_pinhole *= np.sqrt(2)*pinhole_width
    wts_pinhole /= np.sqrt(np.pi)

    #Pinhole hermgauss first:
    for yp, wp in zip(y_pinhole, wts_pinhole):
        rho = np.sqrt(xg*xg + (yg-yp)*(yg-yp))
        phi = np.arctan2(yg,xg)

        hsym, hasym = get_hsym_asym(rho,zg,get_hdet = False, **kwargs)
        hilm += wp*(hsym + np.cos(2*(phi-polar_angle))*hasym)

    #Now line hermgauss
    for a in range(x_vals.size):
        hilm[...,a] *= wts[a]

    return hilm.sum(axis=-1)*2.