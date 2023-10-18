def get_Kprefactor(z, cos_theta, zint=100.0, n2n1=0.95, get_hdet=False,
        **kwargs):
    """
    Returns a prefactor in the electric field integral.

    This is an internal function called by get_K. The returned prefactor
    in the integrand is independent of which integral is being called;
    it is a combination of the exp(1j*phase) and apodization.

    Parameters
    ----------
        z : numpy.ndarray
            The values of z (distance along optical axis) at which to
            calculate the prefactor. Size is unrelated to the size of
            `cos_theta`
        cos_theta : numpy.ndarray
            The values of cos(theta) (i.e. position on the incoming
            focal spherical wavefront) at which to calculate the
            prefactor. Size is unrelated to the size of `z`
        zint : Float, optional
            The position of the optical interface, in units of 1/k.
            Default is 100.
        n2n1 : Float, optional
            The ratio of the index mismatch between the optics (n1) and
            the sample (n2). Default is 0.95
        get_hdet : Bool, optional
            Set to True to calculate the detection prefactor vs the
            illumination prefactor (i.e. False to include apodization).
            Default is False

    Returns
    -------
        numpy.ndarray
            The prefactor, of size [`z.size`, `cos_theta.size`], sampled
            at the values [`z`, `cos_theta`]
    """
    phase = f_theta(cos_theta, zint, z, n2n1=n2n1, **kwargs)
    to_return = np.exp(-1j*phase)
    if not get_hdet:
        to_return *= np.outer(np.ones_like(z),np.sqrt(cos_theta))

    return to_return