def xmatch_basic(ra1, dec1, ra2, dec2, match_radius=5.0):
    '''Finds the closest object in (`ra2`, `dec2`) to scalar coordinate pair
    (`ra1`, `dec1`) and returns the distance in arcseconds.

    This is a quick matcher that uses the `great_circle_dist` function to find
    the closest object in (`ra2`, `dec2`) within `match_radius` arcseconds to
    (`ra1`, `dec1`). (`ra1`, `dec1`) must be a scalar pair, while
    (`ra2`, `dec2`) must be array-likes of the same lengths.

    Parameters
    ----------

    ra1,dec1 : float
        Coordinate of the object to find matches to. In decimal degrees.

    ra2,dec2 : array-like
        The coordinates that will be searched for matches. In decimal degrees.

    match_radius : float
        The match radius in arcseconds to use for the match.

    Returns
    -------

    tuple
        A two element tuple like the following::

            (True -> no match found or False -> found a match,
             minimum distance between target and list in arcseconds)

    '''

    min_dist_arcsec = np.min(great_circle_dist(ra1,dec1,ra2,dec2))

    if (min_dist_arcsec < match_radius):
        return (True,min_dist_arcsec)
    else:
        return (False,min_dist_arcsec)