def equatorial_to_galactic(ra, decl, equinox='J2000'):
    '''This converts from equatorial coords to galactic coords.

    Parameters
    ----------

    ra : float or array-like
        Right ascension values(s) in decimal degrees.

    decl : float or array-like
        Declination value(s) in decimal degrees.

    equinox : str
        The equinox that the coordinates are measured at. This must be
        recognizable by Astropy's `SkyCoord` class.

    Returns
    -------

    tuple of (float, float) or tuple of (np.array, np.array)
        The galactic coordinates (l, b) for each element of the input
        (`ra`, `decl`).

    '''

    # convert the ra/decl to gl, gb
    radecl = SkyCoord(ra=ra*u.degree, dec=decl*u.degree, equinox=equinox)

    gl = radecl.galactic.l.degree
    gb = radecl.galactic.b.degree

    return gl, gb