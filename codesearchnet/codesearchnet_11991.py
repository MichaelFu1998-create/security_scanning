def coord_features(objectinfo):

    '''Calculates object coordinates features, including:

    - galactic coordinates
    - total proper motion from pmra, pmdecl
    - reduced J proper motion from propermotion and Jmag

    Parameters
    ----------

    objectinfo : dict
        This is an objectinfo dict from a light curve file read into an
        `lcdict`. The format and the minimum keys required are::

            {'ra': the right ascension of the object in decimal degrees,
             'decl': the declination of the object in decimal degrees,
             'pmra': the proper motion in right ascension in mas/yr,
             'pmdecl': the proper motion in declination in mas/yr,
             'jmag': the 2MASS J mag of this object}

    Returns
    -------

    dict
        A dict containing the total proper motion

    '''

    retdict = {'propermotion': np.nan,
               'gl':np.nan,
               'gb':np.nan,
               'rpmj':np.nan}

    if ('ra' in objectinfo and
        objectinfo['ra'] is not None and
        np.isfinite(objectinfo['ra']) and
        'decl' in objectinfo and
        objectinfo['decl'] is not None and
        np.isfinite(objectinfo['decl'])):

        retdict['gl'], retdict['gb'] = coordutils.equatorial_to_galactic(
            objectinfo['ra'],
            objectinfo['decl']
        )

    if ('pmra' in objectinfo and
        objectinfo['pmra'] is not None and
        np.isfinite(objectinfo['pmra']) and
        'pmdecl' in objectinfo and
        objectinfo['pmdecl'] is not None and
        np.isfinite(objectinfo['pmdecl']) and
        'decl' in objectinfo and
        objectinfo['decl'] is not None and
        np.isfinite(objectinfo['decl'])):

        retdict['propermotion'] = coordutils.total_proper_motion(
            objectinfo['pmra'],
            objectinfo['pmdecl'],
            objectinfo['decl']
        )

    if ('jmag' in objectinfo and
        objectinfo['jmag'] is not None and
        np.isfinite(objectinfo['jmag']) and
        np.isfinite(retdict['propermotion'])):

        retdict['rpmj'] = coordutils.reduced_proper_motion(
            objectinfo['jmag'],
            retdict['propermotion']
        )

    return retdict