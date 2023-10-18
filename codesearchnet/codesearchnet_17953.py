def calc_pts_hg(npts=20):
    """Returns Hermite-Gauss quadrature points for even functions"""
    pts_hg, wts_hg = np.polynomial.hermite.hermgauss(npts*2)
    pts_hg = pts_hg[npts:]
    wts_hg = wts_hg[npts:] * np.exp(pts_hg*pts_hg)
    return pts_hg, wts_hg