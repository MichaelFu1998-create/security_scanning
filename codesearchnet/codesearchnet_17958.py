def get_hsym_asym(rho, z, get_hdet=False, include_K3_det=True, **kwargs):
    """
    Calculates the symmetric and asymmetric portions of a confocal PSF.

    Parameters
    ----------
        rho : numpy.ndarray
            Rho in cylindrical coordinates, in units of 1/k.
        z : numpy.ndarray
            Z in cylindrical coordinates, in units of 1/k. Must be the
            same shape as `rho`
        get_hdet : Bool, optional
            Set to True to get the detection portion of the psf; False
            to get the illumination portion of the psf. Default is True
        include_K3_det : Bool, optional.
            Flag to not calculate the `K3' component for the detection
            PSF, corresponding to (I think) a low-aperature focusing
            lens and no z-polarization of the focused light. Default
            is True, i.e. calculates the K3 component as if the focusing
            lens is high-aperture

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
        hsym : numpy.ndarray
            `rho`.shape numpy.array of the symmetric portion of the PSF
        hasym : numpy.ndarray
            `rho`.shape numpy.array of the asymmetric portion of the PSF
    """

    K1, Kprefactor = get_K(rho, z, K=1, get_hdet=get_hdet, Kprefactor=None,
            return_Kprefactor=True, **kwargs)
    K2 = get_K(rho, z, K=2, get_hdet=get_hdet, Kprefactor=Kprefactor,
            return_Kprefactor=False, **kwargs)

    if get_hdet and not include_K3_det:
        K3 = 0*K1
    else:
        K3 = get_K(rho, z, K=3, get_hdet=get_hdet, Kprefactor=Kprefactor,
            return_Kprefactor=False, **kwargs)

    hsym = K1*K1.conj() + K2*K2.conj() + 0.5*(K3*K3.conj())
    hasym= K1*K2.conj() + K2*K1.conj() + 0.5*(K3*K3.conj())

    return hsym.real, hasym.real