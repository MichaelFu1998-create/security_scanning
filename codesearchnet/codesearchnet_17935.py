def exact_volume_sphere(rvec, pos, radius, zscale=1.0, volume_error=1e-5,
        function=sphere_analytical_gaussian, max_radius_change=1e-2, args=()):
    """
    Perform an iterative method to calculate the effective sphere that perfectly
    (up to the volume_error) conserves volume.  Return the resulting image
    """
    vol_goal = 4./3*np.pi*radius**3 / zscale
    rprime = radius

    dr = inner(rvec, pos, rprime, zscale=zscale)
    t = function(dr, rprime, *args)
    for i in range(MAX_VOLUME_ITERATIONS):
        vol_curr = np.abs(t.sum())
        if np.abs(vol_goal - vol_curr)/vol_goal < volume_error:
            break

        rprime = rprime + 1.0*(vol_goal - vol_curr) / (4*np.pi*rprime**2)

        if np.abs(rprime - radius)/radius > max_radius_change:
            break

        dr = inner(rvec, pos, rprime, zscale=zscale)
        t = function(dr, rprime, *args)

    return t