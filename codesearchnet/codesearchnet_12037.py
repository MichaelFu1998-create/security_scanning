def xmatch_neighbors(ra1, dec1,
                     ra2, dec2,
                     match_radius=60.0,
                     includeself=False,
                     sortresults=True):
    '''Finds the closest objects in (`ra2`, `dec2`) to scalar coordinate pair
    (`ra1`, `dec1`) and returns the indices of the objects that match.

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

    includeself : bool
        If this is True, the object itself will be included in the match
        results.

    sortresults : bool
        If this is True, the match indices will be sorted by distance.

    Returns
    -------

    tuple
        A tuple like the following is returned::

            (True -> matches found or False -> no matches found,
             minimum distance between target and list,
             np.array of indices where list of coordinates is
             closer than `match_radius` arcseconds from the target,
             np.array of distances in arcseconds)

    '''

    dist = great_circle_dist(ra1,dec1,ra2,dec2)

    if includeself:
        match_dist_ind = np.where(dist < match_radius)

    else:
        # make sure we match only objects that are not the same as this object
        match_dist_ind = np.where((dist < match_radius) & (dist > 0.1))

    if len(match_dist_ind) > 0:
        match_dists = dist[match_dist_ind]
        dist_sort_ind = np.argsort(match_dists)

        if sortresults:
            match_dist_ind = (match_dist_ind[0])[dist_sort_ind]

        min_dist = np.min(match_dists)

        return (True,min_dist,match_dist_ind,match_dists[dist_sort_ind])

    else:
        return (False,)