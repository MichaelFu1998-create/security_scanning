def total_proper_motion(pmra, pmdecl, decl):

    '''This calculates the total proper motion of an object.

    Parameters
    ----------

    pmra : float or array-like
        The proper motion(s) in right ascension, measured in mas/yr.

    pmdecl : float or array-like
        The proper motion(s) in declination, measured in mas/yr.

    decl : float or array-like
        The declination of the object(s) in decimal degrees.

    Returns
    -------

    float or array-like
        The total proper motion(s) of the object(s) in mas/yr.

    '''

    pm = np.sqrt( pmdecl*pmdecl + pmra*pmra*np.cos(np.radians(decl)) *
                  np.cos(np.radians(decl)) )
    return pm