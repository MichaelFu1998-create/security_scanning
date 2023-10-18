def get_K(rho, z, alpha=1.0, zint=100.0, n2n1=0.95, get_hdet=False, K=1,
        Kprefactor=None, return_Kprefactor=False, npts=20, **kwargs):
    """
    Calculates one of three electric field integrals.

    Internal function for calculating point spread functions. Returns
    one of three electric field integrals that describe the electric
    field near the focus of a lens; these integrals appear in Hell's psf
    calculation.

    Parameters
    ----------
        rho : numpy.ndarray
            Rho in cylindrical coordinates, in units of 1/k.
        z : numpy.ndarray
            Z in cylindrical coordinates, in units of 1/k. `rho` and
            `z` must be the same shape

        alpha : Float, optional
            The acceptance angle of the lens, on (0,pi/2). Default is 1.
        zint : Float, optional
            The distance of the len's unaberrated focal point from the
            optical interface, in units of 1/k. Default is 100.
        n2n1 : Float, optional
            The ratio n2/n1 of the index mismatch between the sample
            (index n2) and the optical train (index n1). Must be on
            [0,inf) but should be near 1. Default is 0.95
        get_hdet : Bool, optional
            Set to True to get the detection portion of the psf; False
            to get the illumination portion of the psf. Default is True
        K : {1, 2, 3}, optional
            Which of the 3 integrals to evaluate. Default is 1
        Kprefactor : numpy.ndarray or None
            This array is calculated internally and optionally returned;
            pass it back to avoid recalculation and increase speed. Default
            is None, i.e. calculate it internally.
        return_Kprefactor : Bool, optional
            Set to True to also return the Kprefactor (parameter above)
            to speed up the calculation for the next values of K. Default
            is False
        npts : Int, optional
            The number of points to use for Gauss-Legendre quadrature of
            the integral. Default is 20, which is a good number for x,y,z
            less than 100 or so.

    Returns
    -------
        kint : numpy.ndarray
            The integral K_i; rho.shape numpy.array
        [, Kprefactor] : numpy.ndarray
            The prefactor that is independent of which integral is being
            calculated but does depend on the parameters; can be passed
            back to the function for speed.

    Notes
    -----
        npts=20 gives double precision (no difference between 20, 30, and
        doing all the integrals with scipy.quad). The integrals are only
        over the acceptance angle of the lens, so for moderate x,y,z they
        don't vary too rapidly. For x,y,z, zint large compared to 100, a
        higher npts might be necessary.
    """
    # Comments:
        # This is the only function that relies on rho,z being numpy.arrays,
        # and it's just in a flag that I've added.... move to psf?
    if type(rho) != np.ndarray or type(z) != np.ndarray or (rho.shape != z.shape):
        raise ValueError('rho and z must be np.arrays of same shape.')

    pts, wts = np.polynomial.legendre.leggauss(npts)
    n1n2 = 1.0/n2n1

    rr = np.ravel(rho)
    zr = np.ravel(z)

    #Getting the array of points to quad at
    cos_theta = 0.5*(1-np.cos(alpha))*pts+0.5*(1+np.cos(alpha))
    #[cos_theta,rho,z]

    if Kprefactor is None:
        Kprefactor = get_Kprefactor(z, cos_theta, zint=zint, \
            n2n1=n2n1,get_hdet=get_hdet, **kwargs)

    if K==1:
        part_1 = j0(np.outer(rr,np.sqrt(1-cos_theta**2)))*\
            np.outer(np.ones_like(rr), 0.5*(get_taus(cos_theta,n2n1=n2n1)+\
            get_taup(cos_theta,n2n1=n2n1)*csqrt(1-n1n2**2*(1-cos_theta**2))))
        integrand = Kprefactor * part_1
    elif K==2:
        part_2=j2(np.outer(rr,np.sqrt(1-cos_theta**2)))*\
            np.outer(np.ones_like(rr),0.5*(get_taus(cos_theta,n2n1=n2n1)-\
            get_taup(cos_theta,n2n1=n2n1)*csqrt(1-n1n2**2*(1-cos_theta**2))))
        integrand = Kprefactor * part_2
    elif K==3:
        part_3=j1(np.outer(rho,np.sqrt(1-cos_theta**2)))*\
            np.outer(np.ones_like(rr), n1n2*get_taup(cos_theta,n2n1=n2n1)*\
            np.sqrt(1-cos_theta**2))
        integrand = Kprefactor * part_3
    else:
        raise ValueError('K=1,2,3 only...')

    big_wts=np.outer(np.ones_like(rr), wts)
    kint = (big_wts*integrand).sum(axis=1) * 0.5*(1-np.cos(alpha))

    if return_Kprefactor:
        return kint.reshape(rho.shape), Kprefactor
    else:
        return kint.reshape(rho.shape)