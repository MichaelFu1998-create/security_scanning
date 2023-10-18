def get_polydisp_pts_wts(kfki, sigkf, dist_type='gaussian', nkpts=3):
    """
    Calculates a set of Gauss quadrature points & weights for polydisperse
    light.

    Returns a list of points and weights of the final wavevector's distri-
    bution, in units of the initial wavevector.

    Parameters
    ----------
        kfki : Float
            The mean of the polydisperse outgoing wavevectors.
        sigkf : Float
            The standard dev. of the polydisperse outgoing wavevectors.
        dist_type : {`gaussian`, `gamma`}, optional
            The distribution, gaussian or gamma, of the wavevectors.
            Default is `gaussian`
        nkpts : Int, optional
            The number of quadrature points to use. Default is 3
    Returns
    -------
        kfkipts : numpy.ndarray
            The Gauss quadrature points at which to calculate kfki.
        wts : numpy.ndarray
            The associated Gauss quadrature weights.
    """
    if dist_type.lower() == 'gaussian':
        pts, wts = np.polynomial.hermite.hermgauss(nkpts)
        kfkipts = np.abs(kfki + sigkf*np.sqrt(2)*pts)
    elif dist_type.lower() == 'laguerre' or dist_type.lower() == 'gamma':
        k_scale = sigkf**2/kfki
        associated_order = kfki**2/sigkf**2 - 1
        #Associated Laguerre with alpha >~170 becomes numerically unstable, so:
        max_order=150
        if associated_order > max_order or associated_order < (-1+1e-3):
            warnings.warn('Numerically unstable sigk, clipping', RuntimeWarning)
            associated_order = np.clip(associated_order, -1+1e-3, max_order)
        kfkipts, wts = la_roots(nkpts, associated_order)
        kfkipts *= k_scale
    else:
        raise ValueError('dist_type must be either gaussian or laguerre')
    return kfkipts, wts/wts.sum()