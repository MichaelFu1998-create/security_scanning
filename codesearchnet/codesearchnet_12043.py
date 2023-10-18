def galactic_to_equatorial(gl, gb):
    '''This converts from galactic coords to equatorial coordinates.

    Parameters
    ----------

    gl : float or array-like
        Galactic longitude values(s) in decimal degrees.

    gb : float or array-like
        Galactic latitude value(s) in decimal degrees.

    Returns
    -------

    tuple of (float, float) or tuple of (np.array, np.array)
        The equatorial coordinates (RA, DEC) for each element of the input
        (`gl`, `gb`) in decimal degrees. These are reported in the ICRS frame.

    '''

    gal = SkyCoord(gl*u.degree, gl*u.degree, frame='galactic')

    transformed = gal.transform_to('icrs')

    return transformed.ra.degree, transformed.dec.degree