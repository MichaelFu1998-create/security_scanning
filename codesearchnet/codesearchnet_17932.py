def sphere_analytical_gaussian_trim(dr, a, alpha=0.2765, cut=1.6):
    """
    See sphere_analytical_gaussian_exact.

    I trimmed to terms from the functional form that are essentially zero (1e-8)
    for r0 > cut (~1.5), a fine approximation for these platonic anyway.
    """
    m = np.abs(dr) <= cut

    # only compute on the relevant scales
    rr = dr[m]
    t = -rr/(alpha*np.sqrt(2))
    q = 0.5*(1 + erf(t)) - np.sqrt(0.5/np.pi)*(alpha/(rr+a+1e-10)) * np.exp(-t*t)

    # fill in the grid, inside the interpolation and outside where values are constant
    ans = 0*dr
    ans[m] = q
    ans[dr >  cut] = 0
    ans[dr < -cut] = 1
    return ans