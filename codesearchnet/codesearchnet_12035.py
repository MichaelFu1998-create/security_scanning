def great_circle_dist(ra1, dec1, ra2, dec2):
    '''Calculates the great circle angular distance between two coords.

    This calculates the great circle angular distance in arcseconds between two
    coordinates (ra1,dec1) and (ra2,dec2). This is basically a clone of GCIRC
    from the IDL Astrolib.

    Parameters
    ----------

    ra1,dec1 : float or array-like
        The first coordinate's right ascension and declination value(s) in
        decimal degrees.

    ra2,dec2 : float or array-like
        The second coordinate's right ascension and declination value(s) in
        decimal degrees.

    Returns
    -------

    float or array-like
        Great circle distance between the two coordinates in arseconds.

    Notes
    -----

    If (`ra1`, `dec1`) is scalar and (`ra2`, `dec2`) is scalar: the result is a
    float distance in arcseconds.

    If (`ra1`, `dec1`) is scalar and (`ra2`, `dec2`) is array-like: the result
    is an np.array with distance in arcseconds between (`ra1`, `dec1`) and each
    element of (`ra2`, `dec2`).

    If (`ra1`, `dec1`) is array-like and (`ra2`, `dec2`) is scalar: the result
    is an np.array with distance in arcseconds between (`ra2`, `dec2`) and each
    element of (`ra1`, `dec1`).

    If (`ra1`, `dec1`) and (`ra2`, `dec2`) are both array-like: the result is an
    np.array with the pair-wise distance in arcseconds between each element of
    the two coordinate lists. In this case, if the input array-likes are not the
    same length, then excess elements of the longer one will be ignored.

    '''

    # wrap RA if negative or larger than 360.0 deg
    in_ra1 = ra1 % 360.0
    in_ra1 = in_ra1 + 360.0*(in_ra1 < 0.0)
    in_ra2 = ra2 % 360.0
    in_ra2 = in_ra2 + 360.0*(in_ra1 < 0.0)

    # convert to radians
    ra1_rad, dec1_rad = np.deg2rad(in_ra1), np.deg2rad(dec1)
    ra2_rad, dec2_rad = np.deg2rad(in_ra2), np.deg2rad(dec2)

    del_dec2 = (dec2_rad - dec1_rad)/2.0
    del_ra2 = (ra2_rad - ra1_rad)/2.0
    sin_dist = np.sqrt(np.sin(del_dec2) * np.sin(del_dec2) +
                       np.cos(dec1_rad) * np.cos(dec2_rad) *
                       np.sin(del_ra2) * np.sin(del_ra2))

    dist_rad = 2.0 * np.arcsin(sin_dist)

    # return the distance in arcseconds
    return np.rad2deg(dist_rad)*3600.0