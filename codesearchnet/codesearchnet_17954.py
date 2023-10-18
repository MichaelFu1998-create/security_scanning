def calc_pts_lag(npts=20):
    """
    Returns Gauss-Laguerre quadrature points rescaled for line scan integration

    Parameters
    ----------
        npts : {15, 20, 25}, optional
            The number of points to

    Notes
    -----
        The scale is set internally as the best rescaling for a line scan
        integral; it was checked numerically for the allowed npts.
        Acceptable pts/scls/approximate line integral scan error:
        (pts,   scl  )      :         ERR
        ------------------------------------
        (15, 0.072144)      :       0.002193
        (20, 0.051532)      :       0.001498
        (25, 0.043266)      :       0.001209

        The previous HG(20) error was ~0.13ish
    """
    scl = { 15:0.072144,
            20:0.051532,
            25:0.043266}[npts]
    pts0, wts0 = np.polynomial.laguerre.laggauss(npts)
    pts = np.sinh(pts0*scl)
    wts = scl*wts0*np.cosh(pts0*scl)*np.exp(pts0)
    return pts, wts