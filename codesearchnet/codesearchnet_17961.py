def calculate_polychrome_pinhole_psf(x, y, z, normalize=False, kfki=0.889,
        sigkf=0.1, zint=100., nkpts=3, dist_type='gaussian', **kwargs):
    """
    Calculates the perfect-pinhole PSF, for a set of points (x,y,z).

    Parameters
    -----------
        x : numpy.ndarray
            The x-coordinate of the PSF in units of 1/ the wavevector of
            the incoming light.
        y : numpy.ndarray
            The y-coordinate.
        z : numpy.ndarray
            The z-coordinate.
        kfki : Float
            The mean ratio of the outgoing light's wavevector to the incoming
            light's. Default is 0.89.
        sigkf : Float
            Standard deviation of kfki; the distribution of the light values
            will be approximately kfki +- sigkf.
        zint : Float
            The (scalar) distance from the interface, in units of
            1/k_incoming. Default is 100.0
        dist_type: The distribution type of the polychromatic light.
            Can be one of 'laguerre'/'gamma' or 'gaussian.' If 'gaussian'
            the resulting k-values are taken in absolute value. Default
            is 'gaussian.'
        normalize : Bool
            Set to True to normalize the psf correctly, accounting for
            intensity variations with depth. This will give a psf that does
            not sum to 1. Default is False.

    Other Parameters
    ----------------
        alpha : Float
            The opening angle of the lens. Default is 1.
        n2n1 : Float
            The ratio of the index in the 2nd medium to that in the first.
            Default is 0.95

    Returns
    -------
        psf : numpy.ndarray, of shape x.shape

    Comments
    --------
        (1) The PSF is not necessarily centered on the z=0 pixel, since the
            calculation includes the shift.

        (2) If you want z-varying illumination of the psf then set
            normalize=True. This does the normalization by doing:
                hsym, hasym /= hsym.sum()
                hdet /= hdet.sum()
            and then calculating the psf that way. So if you want the
            intensity to be correct you need to use a large-ish array of
            roughly equally spaced points. Or do it manually by calling
            get_hsym_asym()
    """
    #0. Setup
    kfkipts, wts = get_polydisp_pts_wts(kfki, sigkf, dist_type=dist_type,
            nkpts=nkpts)
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)

    #1. Hilm
    hsym, hasym = get_hsym_asym(rho, z, zint=zint, get_hdet=False, **kwargs)
    hilm = (hsym + np.cos(2*phi)*hasym)

    #2. Hdet
    hdet_func = lambda kfki: get_hsym_asym(rho*kfki, z*kfki,
                zint=kfki*zint, get_hdet=True, **kwargs)[0]
    inner = [wts[a] * hdet_func(kfkipts[a]) for a in range(nkpts)]
    hdet = np.sum(inner, axis=0)

    #3. Normalize and return
    if normalize:
        hilm /= hilm.sum()
        hdet /= hdet.sum()
    psf = hdet * hilm
    return psf if normalize else psf / psf.sum()