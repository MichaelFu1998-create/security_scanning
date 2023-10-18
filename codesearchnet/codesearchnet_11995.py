def neighbor_gaia_features(objectinfo,
                           lclist_kdtree,
                           neighbor_radius_arcsec,
                           gaia_matchdist_arcsec=3.0,
                           verbose=True,
                           gaia_submit_timeout=10.0,
                           gaia_submit_tries=3,
                           gaia_max_timeout=180.0,
                           gaia_mirror=None,
                           complete_query_later=True,
                           search_simbad=False):
    '''Gets several neighbor, GAIA, and SIMBAD features:

    From the KD-Tree in the given light curve catalog the object is in:
    `lclist_kdtree`:

    - distance to closest neighbor in arcsec
    - total number of all neighbors within 2 x `neighbor_radius_arcsec`

    From the GAIA DR2 catalog:

    - distance to closest neighbor in arcsec
    - total number of all neighbors within 2 x `neighbor_radius_arcsec`
    - gets the parallax for the object and neighbors
    - calculates the absolute GAIA mag and `G-K` color for use in CMDs
    - gets the proper motion in RA/Dec if available

    From the SIMBAD catalog:

    - the name of the object
    - the type of the object

    Parameters
    ----------

    objectinfo : dict
        This is the objectinfo dict from an object's light curve. This must
        contain at least the following keys::

            {'ra': the right ascension of the object,
             'decl': the declination of the object}

    lclist_kdtree : scipy.spatial.cKDTree object
        This is a KD-Tree built on the Cartesian xyz coordinates from (ra, dec)
        of all objects in the same field as this object. It is similar to that
        produced by :py:func:`astrobase.lcproc.catalogs.make_lclist`, and is
        used to carry out the spatial search required to find neighbors for this
        object.

    neighbor_radius_arcsec : float
        The maximum radius in arcseconds around this object to search for
        neighbors in both the light curve catalog and in the GAIA DR2 catalog.

    gaia_matchdist_arcsec : float
        The maximum distance in arcseconds to use for a GAIA cross-match to this
        object.

    verbose : bool
        If True, indicates progress and warns of problems.

    gaia_submit_timeout : float
        Sets the timeout in seconds to use when submitting a request to look up
        the object's information to the GAIA service. Note that if `fast_mode`
        is set, this is ignored.

    gaia_submit_tries : int
        Sets the maximum number of times the GAIA services will be contacted to
        obtain this object's information. If `fast_mode` is set, this is
        ignored, and the services will be contacted only once (meaning that a
        failure to respond will be silently ignored and no GAIA data will be
        added to the checkplot's objectinfo dict).

    gaia_max_timeout : float
        Sets the timeout in seconds to use when waiting for the GAIA service to
        respond to our request for the object's information. Note that if
        `fast_mode` is set, this is ignored.

    gaia_mirror : str
        This sets the GAIA mirror to use. This is a key in the
        `services.gaia.GAIA_URLS` dict which defines the URLs to hit for each
        mirror.

    search_simbad : bool
        If this is True, searches for objects in SIMBAD at this object's
        location and gets the object's SIMBAD main ID, type, and stellar
        classification if available.

    Returns
    -------

    dict
        Returns a dict with neighbor, GAIA, and SIMBAD features.

    '''

    # kdtree search for neighbors in light curve catalog
    if ('ra' in objectinfo and 'decl' in objectinfo and
        objectinfo['ra'] is not None and objectinfo['decl'] is not None and
        (isinstance(lclist_kdtree, cKDTree) or
         isinstance(lclist_kdtree, KDTree))):

        ra, decl = objectinfo['ra'], objectinfo['decl']

        cosdecl = np.cos(np.radians(decl))
        sindecl = np.sin(np.radians(decl))
        cosra = np.cos(np.radians(ra))
        sinra = np.sin(np.radians(ra))

        # this is the search distance in xyz unit vectors
        xyzdist = 2.0 * np.sin(np.radians(neighbor_radius_arcsec/3600.0)/2.0)

        # look up the coordinates for the closest 100 objects in the kdtree
        # within 2 x neighbor_radius_arcsec
        kdt_dist, kdt_ind = lclist_kdtree.query(
            [cosra*cosdecl,
             sinra*cosdecl,
             sindecl],
            k=100,
            distance_upper_bound=xyzdist
        )

        # the first match is the object itself
        finite_distind = (np.isfinite(kdt_dist)) & (kdt_dist > 0)
        finite_dists = kdt_dist[finite_distind]
        nbrindices = kdt_ind[finite_distind]
        n_neighbors = finite_dists.size

        if n_neighbors > 0:

            closest_dist = finite_dists.min()
            closest_dist_arcsec = (
                np.degrees(2.0*np.arcsin(closest_dist/2.0))*3600.0
            )
            closest_dist_nbrind = nbrindices[finite_dists == finite_dists.min()]

            resultdict = {
                'neighbors':n_neighbors,
                'nbrindices':nbrindices,
                'distarcsec':np.degrees(2.0*np.arcsin(finite_dists/2.0))*3600.0,
                'closestdistarcsec':closest_dist_arcsec,
                'closestdistnbrind':closest_dist_nbrind,
                'searchradarcsec':neighbor_radius_arcsec,
            }

        else:

            resultdict = {
                'neighbors':0,
                'nbrindices':np.array([]),
                'distarcsec':np.array([]),
                'closestdistarcsec':np.nan,
                'closestdistnbrind':np.array([]),
                'searchradarcsec':neighbor_radius_arcsec,
            }


    else:
        if verbose:
            LOGWARNING("one of ra, decl, kdtree is missing in "
                       "objectinfo dict or lclistpkl, "
                       "can't get observed neighbors")

        resultdict = {
            'neighbors':np.nan,
            'nbrindices':np.array([]),
            'distarcsec':np.array([]),
            'closestdistarcsec':np.nan,
            'closestdistnbrind':np.array([]),
            'searchradarcsec':neighbor_radius_arcsec,
        }


    # next, search for this object in GAIA
    if ('ra' in objectinfo and 'decl' in objectinfo and
        objectinfo['ra'] is not None and objectinfo['decl'] is not None):

        gaia_result = gaia.objectlist_conesearch(
            objectinfo['ra'],
            objectinfo['decl'],
            neighbor_radius_arcsec,
            verbose=verbose,
            timeout=gaia_submit_timeout,
            maxtimeout=gaia_max_timeout,
            maxtries=gaia_submit_tries,
            gaia_mirror=gaia_mirror,
            complete_query_later=complete_query_later
        )

        if gaia_result:

            gaia_objlistf = gaia_result['result']

            with gzip.open(gaia_objlistf,'rb') as infd:

                try:
                    gaia_objlist = np.genfromtxt(
                        infd,
                        names=True,
                        delimiter=',',
                        dtype='U20,f8,f8,f8,f8,f8,f8,f8,f8,f8,f8,f8,f8',
                        usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12)
                    )
                except Exception as e:
                    gaia_objlist = []

            gaia_objlist = np.atleast_1d(gaia_objlist)

            if gaia_objlist.size > 0:

                # if we have GAIA results, we can get xypositions of all of
                # these objects on the object skyview stamp
                stampres = skyview.get_stamp(objectinfo['ra'],
                                             objectinfo['decl'])

                if (stampres and
                    'fitsfile' in stampres and
                    stampres['fitsfile'] is not None and
                    os.path.exists(stampres['fitsfile'])):

                    stampwcs = WCS(stampres['fitsfile'])

                    gaia_xypos = stampwcs.all_world2pix(
                        np.column_stack((gaia_objlist['ra'],
                                         gaia_objlist['dec'])),
                        1
                    )

                else:

                    gaia_xypos = None


                # the first object is likely the match to the object itself
                if gaia_objlist['dist_arcsec'][0] < gaia_matchdist_arcsec:

                    if gaia_objlist.size > 1:

                        gaia_nneighbors = gaia_objlist[1:].size

                        gaia_status = (
                            'ok: object found with %s neighbors' %
                            gaia_nneighbors
                        )

                        # the first in each array is the object
                        gaia_ids = gaia_objlist['source_id']
                        gaia_mags = gaia_objlist['phot_g_mean_mag']
                        gaia_parallaxes = gaia_objlist['parallax']
                        gaia_parallax_errs = gaia_objlist['parallax_error']
                        gaia_pmra = gaia_objlist['pmra']
                        gaia_pmra_err = gaia_objlist['pmra_error']
                        gaia_pmdecl = gaia_objlist['pmdec']
                        gaia_pmdecl_err = gaia_objlist['pmdec_error']

                        gaia_absolute_mags = magnitudes.absolute_gaia_magnitude(
                            gaia_mags, gaia_parallaxes
                        )
                        if ('kmag' in objectinfo and
                            objectinfo['kmag'] is not None and
                            np.isfinite(objectinfo['kmag'])):
                            gaiak_colors = gaia_mags - objectinfo['kmag']
                        else:
                            gaiak_colors = None

                        gaia_dists = gaia_objlist['dist_arcsec']
                        gaia_closest_distarcsec = gaia_objlist['dist_arcsec'][1]
                        gaia_closest_gmagdiff = (
                            gaia_objlist['phot_g_mean_mag'][0] -
                            gaia_objlist['phot_g_mean_mag'][1]
                        )

                    else:

                        LOGWARNING('object found in GAIA at (%.3f,%.3f), '
                                   'but no neighbors' % (objectinfo['ra'],
                                                         objectinfo['decl']))

                        gaia_nneighbors = 0

                        gaia_status = (
                            'ok: object found but no neighbors'
                        )

                        # the first in each array is the object
                        gaia_ids = gaia_objlist['source_id']
                        gaia_mags = gaia_objlist['phot_g_mean_mag']
                        gaia_parallaxes = gaia_objlist['parallax']
                        gaia_parallax_errs = gaia_objlist['parallax_error']
                        gaia_pmra = gaia_objlist['pmra']
                        gaia_pmra_err = gaia_objlist['pmra_error']
                        gaia_pmdecl = gaia_objlist['pmdec']
                        gaia_pmdecl_err = gaia_objlist['pmdec_error']

                        gaia_absolute_mags = magnitudes.absolute_gaia_magnitude(
                            gaia_mags, gaia_parallaxes
                        )
                        if ('kmag' in objectinfo and
                            objectinfo['kmag'] is not None and
                            np.isfinite(objectinfo['kmag'])):
                            gaiak_colors = gaia_mags - objectinfo['kmag']
                        else:
                            gaiak_colors = None

                        gaia_dists = gaia_objlist['dist_arcsec']
                        gaia_closest_distarcsec = np.nan
                        gaia_closest_gmagdiff = np.nan


                # otherwise, the object wasn't found in GAIA for some reason
                else:

                    LOGWARNING('no GAIA objects found within '
                               '%.3f arcsec of object position (%.3f, %.3f), '
                               'closest object is at %.3f arcsec away' %
                               (gaia_matchdist_arcsec,
                                objectinfo['ra'], objectinfo['decl'],
                                gaia_objlist['dist_arcsec'][0]))

                    gaia_status = ('failed: no object within %.3f '
                                   'arcsec, closest = %.3f arcsec' %
                                   (gaia_matchdist_arcsec,
                                    gaia_objlist['dist_arcsec'][0]))

                    gaia_nneighbors = np.nan

                    gaia_ids = gaia_objlist['source_id']
                    gaia_mags = gaia_objlist['phot_g_mean_mag']
                    gaia_parallaxes = gaia_objlist['parallax']
                    gaia_parallax_errs = gaia_objlist['parallax_error']
                    gaia_pmra = gaia_objlist['pmra']
                    gaia_pmra_err = gaia_objlist['pmra_error']
                    gaia_pmdecl = gaia_objlist['pmdec']
                    gaia_pmdecl_err = gaia_objlist['pmdec_error']

                    gaia_absolute_mags = magnitudes.absolute_gaia_magnitude(
                        gaia_mags, gaia_parallaxes
                    )
                    if ('kmag' in objectinfo and
                        objectinfo['kmag'] is not None and
                        np.isfinite(objectinfo['kmag'])):
                        gaiak_colors = gaia_mags - objectinfo['kmag']
                    else:
                        gaiak_colors = None

                    gaia_dists = gaia_objlist['dist_arcsec']
                    gaia_closest_distarcsec = np.nan
                    gaia_closest_gmagdiff = np.nan

            # if there are no neighbors within neighbor_radius_arcsec
            # or this object is not covered by GAIA. return nothing
            else:

                LOGERROR('no GAIA objects at this '
                         'position or GAIA query failed')

                gaia_status = (
                    'failed: no GAIA objects at this '
                    'position or GAIA query failed.'
                )
                gaia_nneighbors = np.nan
                gaia_ids = None
                gaia_mags = None

                gaia_xypos = None
                gaia_parallaxes = None
                gaia_parallax_errs = None
                gaia_pmra = None
                gaia_pmra_err = None
                gaia_pmdecl = None
                gaia_pmdecl_err = None
                gaia_absolute_mags = None
                gaiak_colors = None

                gaia_dists = None
                gaia_closest_distarcsec = np.nan
                gaia_closest_gmagdiff = np.nan

            # update the resultdict with gaia stuff
            resultdict.update(
                {'gaia_status':gaia_status,
                 'gaia_neighbors':gaia_nneighbors,
                 'gaia_ids':gaia_ids,
                 'gaia_xypos':gaia_xypos,
                 'gaia_mags':gaia_mags,
                 'gaia_parallaxes':gaia_parallaxes,
                 'gaia_parallax_errs':gaia_parallax_errs,
                 'gaia_pmras':gaia_pmra,
                 'gaia_pmra_errs':gaia_pmra_err,
                 'gaia_pmdecls':gaia_pmdecl,
                 'gaia_pmdecl_errs':gaia_pmdecl_err,
                 'gaia_absolute_mags':gaia_absolute_mags,
                 'gaiak_colors':gaiak_colors,
                 'gaia_dists':gaia_dists,
                 'gaia_closest_distarcsec':gaia_closest_distarcsec,
                 'gaia_closest_gmagdiff':gaia_closest_gmagdiff}
            )

        else:

            LOGERROR('GAIA query did not return a '
                     'result for object at (%.3f, %.3f)' % (objectinfo['ra'],
                                                            objectinfo['decl']))

            resultdict.update(
                {'gaia_status':'failed: GAIA TAP query failed',
                 'gaia_neighbors':np.nan,
                 'gaia_ids':None,
                 'gaia_xypos':None,
                 'gaia_mags':None,
                 'gaia_parallaxes':None,
                 'gaia_parallax_errs':None,
                 'gaia_pmras':None,
                 'gaia_pmra_errs':None,
                 'gaia_pmdecls':None,
                 'gaia_pmdecl_errs':None,
                 'gaia_absolute_mags':None,
                 'gaiak_colors':None,
                 'gaia_dists':None,
                 'gaia_closest_distarcsec':np.nan,
                 'gaia_closest_gmagdiff':np.nan}
            )


    else:

        LOGERROR("one or more of the 'ra', 'decl' keys "
                 "are missing from the objectinfo dict, "
                 "can't get GAIA or LC collection neighbor features")

        resultdict.update(
            {'gaia_status':'failed: no ra/decl for object',
             'gaia_neighbors':np.nan,
             'gaia_ids':None,
             'gaia_xypos':None,
             'gaia_mags':None,
             'gaia_parallaxes':None,
             'gaia_parallax_errs':None,
             'gaia_pmras':None,
             'gaia_pmra_errs':None,
             'gaia_pmdecls':None,
             'gaia_pmdecl_errs':None,
             'gaia_absolute_mags':None,
             'gaiak_colors':None,
             'gaia_dists':None,
             'gaia_closest_distarcsec':np.nan,
             'gaia_closest_gmagdiff':np.nan}
        )


    # finally, search for this object in SIMBAD
    if ('ra' in objectinfo and 'decl' in objectinfo and
        objectinfo['ra'] is not None and objectinfo['decl'] is not None and
        search_simbad):

        simbad_result = simbad.objectnames_conesearch(
            objectinfo['ra'],
            objectinfo['decl'],
            neighbor_radius_arcsec,
            verbose=verbose,
            timeout=gaia_submit_timeout,
            maxtimeout=gaia_max_timeout,
            maxtries=gaia_submit_tries,
            complete_query_later=complete_query_later
        )

    else:

        simbad_result = None

    if (simbad_result and
        simbad_result['result'] and
        os.path.exists(simbad_result['result'])):

        with gzip.open(simbad_result['result'],'rb') as infd:

            try:
                simbad_objectnames = np.genfromtxt(
                    infd,
                    names=True,
                    delimiter=',',
                    dtype='U20,f8,f8,U20,U20,U20,i8,U600,f8',
                    usecols=(0,1,2,3,4,5,6,7,8),
                    comments='?',
                )
            except Exception as e:
                simbad_objectnames = []

            simbad_objectnames = np.atleast_1d(simbad_objectnames)

            if simbad_objectnames.size > 0:

                simbad_mainid = simbad_objectnames['main_id'].tolist()
                simbad_allids = simbad_objectnames['all_ids'].tolist()
                simbad_objtype = simbad_objectnames['otype_txt'].tolist()
                simbad_distarcsec = simbad_objectnames['dist_arcsec'].tolist()
                simbad_nmatches = len(simbad_mainid)

                simbad_mainid = [x.replace('"','') for x in simbad_mainid]
                simbad_allids = [x.replace('"','') for x in simbad_allids]
                simbad_objtype = [x.replace('"','') for x in simbad_objtype]


                resultdict.update({
                    'simbad_nmatches':simbad_nmatches,
                    'simbad_mainid':simbad_mainid,
                    'simbad_objtype':simbad_objtype,
                    'simbad_allids':simbad_allids,
                    'simbad_distarcsec':simbad_distarcsec
                })


                if simbad_nmatches > 1:

                    resultdict['simbad_status'] = (
                        'ok: multiple SIMBAD matches found'
                    )

                else:

                    resultdict['simbad_status'] = 'ok: single SIMBAD match'



                # get the closest match
                if simbad_distarcsec[0] < gaia_matchdist_arcsec:

                    resultdict.update({
                        'simbad_best_mainid':simbad_mainid[0],
                        'simbad_best_objtype':simbad_objtype[0],
                        'simbad_best_allids':simbad_allids[0],
                        'simbad_best_distarcsec':simbad_distarcsec[0],
                        'simbad_status':'ok: object found within match radius'
                    })

                else:

                    LOGWARNING('no SIMBAD objects found within '
                               '%.3f arcsec of object position (%.3f, %.3f), '
                               'closest object: %s at %.3f arcsec away' %
                               (gaia_matchdist_arcsec,
                                objectinfo['ra'],
                                objectinfo['decl'],
                                simbad_mainid[0],
                                simbad_distarcsec[0]))

                    simbad_status = ('failed: no object within %.3f '
                                     'arcsec, closest = %.3f arcsec' %
                                     (gaia_matchdist_arcsec,
                                      simbad_distarcsec[0]))


                    resultdict.update({
                        'simbad_best_mainid':None,
                        'simbad_best_objtype':None,
                        'simbad_best_allids':None,
                        'simbad_best_distarcsec':None,
                        'simbad_status':simbad_status
                    })


            else:

                resultdict.update({
                    'simbad_status':'failed: no SIMBAD matches found',
                    'simbad_nmatches':None,
                    'simbad_mainid':None,
                    'simbad_objtype':None,
                    'simbad_allids':None,
                    'simbad_distarcsec':None,
                    'simbad_best_mainid':None,
                    'simbad_best_objtype':None,
                    'simbad_best_allids':None,
                    'simbad_best_distarcsec':None,
                })

    else:

        if search_simbad:
            simbad_status = 'failed: SIMBAD query failed'
        else:
            simbad_status = 'failed: SIMBAD query not tried'

        resultdict.update({
            'simbad_status':simbad_status,
            'simbad_nmatches':None,
            'simbad_mainid':None,
            'simbad_objtype':None,
            'simbad_allids':None,
            'simbad_distarcsec':None,
            'simbad_best_mainid':None,
            'simbad_best_objtype':None,
            'simbad_best_allids':None,
            'simbad_best_distarcsec':None,
        })

    return resultdict