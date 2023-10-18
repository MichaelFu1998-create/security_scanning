def calculate_pinhole_psf(x, y, z, kfki=0.89, zint=100.0, normalize=False,
        **kwargs):
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
            The (scalar) ratio of wavevectors of the outgoing light to the
            incoming light. Default is 0.89.
        zint : Float
            The (scalar) distance from the interface, in units of
            1/k_incoming. Default is 100.0
        normalize : Bool
            Set to True to normalize the psf correctly, accounting for
            intensity variations with depth. This will give a psf that does
            not sum to 1.

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
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)

    hsym, hasym = get_hsym_asym(rho, z, zint=zint, get_hdet=False, **kwargs)
    hdet, toss  = get_hsym_asym(rho*kfki, z*kfki, zint=kfki*zint, get_hdet=True, **kwargs)

    if normalize:
        hasym /= hsym.sum()
        hsym /= hsym.sum()
        hdet /= hdet.sum()

    return (hsym + np.cos(2*phi)*hasym)*hdet