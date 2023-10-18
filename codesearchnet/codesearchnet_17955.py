def f_theta(cos_theta, zint, z, n2n1=0.95, sph6_ab=None, **kwargs):
    """
    Returns the wavefront aberration for an aberrated, defocused lens.

    Calculates the portions of the wavefront distortion due to z, theta
    only, for a lens with defocus and spherical aberration induced by
    coverslip mismatch. (The rho portion can be analytically integrated
    to Bessels.)

    Parameters
    ----------
        cos_theta : numpy.ndarray.
            The N values of cos(theta) at which to compute f_theta.
        zint : Float
            The position of the lens relative to the interface.
        z : numpy.ndarray
            The M z-values to compute f_theta at. `z.size` is unrelated
            to `cos_theta.size`
        n2n1: Float, optional
            The ratio of the index of the immersed medium to the optics.
            Default is 0.95
        sph6_ab : Float or None, optional
            Set sph6_ab to a nonzero value to add residual 6th-order
            spherical aberration that is proportional to sph6_ab. Default
            is None (i.e. doesn't calculate).

    Returns
    -------
        wvfront : numpy.ndarray
            The aberrated wavefront, as a function of theta and z.
            Shape is [z.size, cos_theta.size]
    """
    wvfront = (np.outer(np.ones_like(z)*zint, cos_theta) -
            np.outer(zint+z, csqrt(n2n1**2-1+cos_theta**2)))
    if (sph6_ab is not None) and (not np.isnan(sph6_ab)):
        sec2_theta = 1.0/(cos_theta*cos_theta)
        wvfront += sph6_ab * (sec2_theta-1)*(sec2_theta-2)*cos_theta
    #Ensuring evanescent waves are always suppressed:
    if wvfront.dtype == np.dtype('complex128'):
        wvfront.imag = -np.abs(wvfront.imag)
    return wvfront