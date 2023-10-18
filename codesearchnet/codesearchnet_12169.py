def _get_legendre_deg_ctd(npts):
    '''This is a helper function for centroid detrending.

    '''

    from scipy.interpolate import interp1d

    degs = nparray([4,5,6,10,15])
    pts = nparray([1e2,3e2,5e2,1e3,3e3])
    fn = interp1d(pts, degs, kind='linear',
                  bounds_error=False,
                  fill_value=(min(degs), max(degs)))
    legendredeg = int(npfloor(fn(npts)))

    return legendredeg