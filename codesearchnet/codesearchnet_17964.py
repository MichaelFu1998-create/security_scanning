def calculate_linescan_psf(x, y, z, normalize=False, kfki=0.889, zint=100.,
        polar_angle=0., wrap=True, **kwargs):
    """
    Calculates the point spread function of a line-scanning confocal.

    Make x,y,z  __1D__ numpy.arrays, with x the direction along the
    scan line. (to make the calculation faster since I dont' need the line
    ilm for each x).

    Parameters
    ----------
        x : numpy.ndarray
            _One_dimensional_ array of the x grid points (along the line
            illumination) at which to evaluate the psf. In units of
            1/k_incoming.
        y : numpy.ndarray
            _One_dimensional_ array of the y grid points (in plane,
            perpendicular to the line illumination) at which to evaluate
            the psf. In units of 1/k_incoming.
        z : numpy.ndarray
            _One_dimensional_ array of the z grid points (along the
            optical axis) at which to evaluate the psf. In units of
            1/k_incoming.
        normalize : Bool, optional
            Set to True to include the effects of PSF normalization on
            the image intensity. Default is False.
        kfki : Float, optional
            The ratio of the final light's wavevector to the incoming.
            Default is 0.889
        zint : Float, optional
            The position of the optical interface, in units of 1/k_incoming
            Default is 100.
        wrap : Bool, optional
            If True, wraps the psf calculation for speed, assuming that
            the input x, y are regularly-spaced points. If x,y are not
            regularly spaced then `wrap` must be set to False. Default is True.
        polar_angle : Float, optional
            The polarization angle of the light (radians) with respect to
            the line direction (x). Default is 0.

    Other Parameters
    ----------------
        alpha : Float
            The opening angle of the lens. Default is 1.
        n2n1 : Float
            The ratio of the index in the 2nd medium to that in the first.
            Default is 0.95

    Returns
    -------
        numpy.ndarray
            A 3D- numpy.array of the point-spread function. Indexing is
            psf[x,y,z]; shape is [x.size, y,size, z.size]
    """

    #0. Set up vecs
    if wrap:
        xpts = vec_to_halfvec(x)
        ypts = vec_to_halfvec(y)
        x3, y3, z3 = np.meshgrid(xpts, ypts, z, indexing='ij')
    else:
        x3,y3,z3 = np.meshgrid(x, y, z, indexing='ij')
    rho3 = np.sqrt(x3*x3 + y3*y3)

    #1. Hilm
    if wrap:
        y2,z2 = np.meshgrid(ypts, z, indexing='ij')
        hilm0 = calculate_linescan_ilm_psf(y2, z2, zint=zint,
                polar_angle=polar_angle, **kwargs)
        if ypts[0] == 0:
            hilm = np.append(hilm0[-1:0:-1], hilm0, axis=0)
        else:
            hilm = np.append(hilm0[::-1], hilm0, axis=0)
    else:
        y2,z2 = np.meshgrid(y, z, indexing='ij')
        hilm = calculate_linescan_ilm_psf(y2, z2, zint=zint,
                polar_angle=polar_angle, **kwargs)

    #2. Hdet
    if wrap:
        #Lambda function that ignores its args but still returns correct values
        func = lambda *args: get_hsym_asym(rho3*kfki, z3*kfki, zint=kfki*zint,
                    get_hdet=True, **kwargs)[0]
        hdet = wrap_and_calc_psf(xpts, ypts, z, func)
    else:
        hdet, toss = get_hsym_asym(rho3*kfki, z3*kfki, zint=kfki*zint,
                get_hdet=True, **kwargs)

    if normalize:
        hilm /= hilm.sum()
        hdet /= hdet.sum()

    for a in range(x.size):
        hdet[a] *= hilm

    return hdet if normalize else hdet / hdet.sum()