def get_psf_scalar(x, y, z, kfki=1., zint=100.0, normalize=False, **kwargs):
    """
    Calculates a scalar (non-vectorial light) approximation to a confocal PSF

    The calculation is approximate, since it ignores the effects of
    polarization and apodization, but should be ~3x faster.

    Parameters
    ----------
        x : numpy.ndarray
            The x-coordinate of the PSF in units of 1/ the wavevector
            of the incoming light.
        y : numpy.ndarray
            The y-coordinate of the PSF in units of 1/ the wavevector
            of the incoming light. Must be the same shape as `x`.
        z : numpy.ndarray
            The z-coordinate of the PSF in units of 1/ the wavevector
            of the incoming light. Must be the same shape as `x`.
        kfki : Float, optional
            The ratio of wavevectors of the outgoing light to the
            incoming light. Set to 1.0 to speed up the calculation
            by another factor of 2. Default is 1.0
        zint : Float, optional
            The distance from to the optical interface, in units of
            1/k_incoming. Default is 100.
        normalize : Bool
            Set to True to normalize the psf correctly, accounting for
            intensity variations with depth. This will give a psf that does
            not sum to 1. Default is False.
        alpha : Float
            The opening angle of the lens. Default is 1.
        n2n1 : Float
            The ratio of the index in the 2nd medium to that in the first.
            Default is 0.95

    Outputs:
        - psf: x.shape numpy.array.

    Comments:
        (1) Note that the PSF is not necessarily centered on the z=0 pixel,
            since the calculation includes the shift.

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

    K1 = get_K(rho, z, K=1,zint=zint,get_hdet=True, **kwargs)
    hilm = np.real( K1*K1.conj() )

    if np.abs(kfki - 1.0) > 1e-13:
        Kdet = get_K(rho*kfki, z*kfki, K=1, zint=zint*kfki, get_hdet=True,
                **kwargs)
        hdet = np.real( Kdet*Kdet.conj() )
    else:
        hdet = hilm.copy()

    if normalize:
        hilm /= hsym.sum()
        hdet /= hdet.sum()
        psf = hilm * hdet
    else:
        psf = hilm * hdet
        # psf /= psf.sum()

    return psf