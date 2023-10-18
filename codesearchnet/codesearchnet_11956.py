def _pkl_finder_objectinfo(
        objectinfo,
        varinfo,
        findercmap,
        finderconvolve,
        sigclip,
        normto,
        normmingap,
        deredden_object=True,
        custom_bandpasses=None,
        lclistpkl=None,
        nbrradiusarcsec=30.0,
        maxnumneighbors=5,
        plotdpi=100,
        findercachedir='~/.astrobase/stamp-cache',
        verbose=True,
        gaia_submit_timeout=10.0,
        gaia_submit_tries=3,
        gaia_max_timeout=180.0,
        gaia_mirror=None,
        fast_mode=False,
        complete_query_later=True
):
    '''This returns the finder chart and object information as a dict.

    Parameters
    ----------

    objectinfo : dict or None
        If provided, this is a dict containing information on the object whose
        light curve is being processed. This function will then be able to look
        up and download a finder chart for this object and write that to the
        output checkplotdict. External services such as GAIA, SIMBAD, TIC@MAST,
        etc. will also be used to look up this object by its coordinates, and
        will add in information available from those services.

        The `objectinfo` dict must be of the form and contain at least the keys
        described below::

            {'objectid': the name of the object,
             'ra': the right ascension of the object in decimal degrees,
             'decl': the declination of the object in decimal degrees,
             'ndet': the number of observations of this object}

        You can also provide magnitudes and proper motions of the object using
        the following keys and the appropriate values in the `objectinfo`
        dict. These will be used to calculate colors, total and reduced proper
        motion, etc. and display these in the output checkplot PNG::

            'pmra' -> the proper motion in mas/yr in right ascension,
            'pmdecl' -> the proper motion in mas/yr in declination,
            'umag'  -> U mag		 -> colors: U-B, U-V, U-g
            'bmag'  -> B mag		 -> colors: U-B, B-V
            'vmag'  -> V mag		 -> colors: U-V, B-V, V-R, V-I, V-K
            'rmag'  -> R mag		 -> colors: V-R, R-I
            'imag'  -> I mag		 -> colors: g-I, V-I, R-I, B-I
            'jmag'  -> 2MASS J mag	 -> colors: J-H, J-K, g-J, i-J
            'hmag'  -> 2MASS H mag	 -> colors: J-H, H-K
            'kmag'  -> 2MASS Ks mag	 -> colors: g-Ks, H-Ks, J-Ks, V-Ks
            'sdssu' -> SDSS u mag	 -> colors: u-g, u-V
            'sdssg' -> SDSS g mag	 -> colors: g-r, g-i, g-K, u-g, U-g, g-J
            'sdssr' -> SDSS r mag	 -> colors: r-i, g-r
            'sdssi' -> SDSS i mag	 -> colors: r-i, i-z, g-i, i-J, i-W1
            'sdssz' -> SDSS z mag	 -> colors: i-z, z-W2, g-z
            'ujmag' -> UKIRT J mag	 -> colors: J-H, H-K, J-K, g-J, i-J
            'uhmag' -> UKIRT H mag	 -> colors: J-H, H-K
            'ukmag' -> UKIRT K mag	 -> colors: g-K, H-K, J-K, V-K
            'irac1' -> Spitzer IRAC1 mag -> colors: i-I1, I1-I2
            'irac2' -> Spitzer IRAC2 mag -> colors: I1-I2, I2-I3
            'irac3' -> Spitzer IRAC3 mag -> colors: I2-I3
            'irac4' -> Spitzer IRAC4 mag -> colors: I3-I4
            'wise1' -> WISE W1 mag	 -> colors: i-W1, W1-W2
            'wise2' -> WISE W2 mag	 -> colors: W1-W2, W2-W3
            'wise3' -> WISE W3 mag	 -> colors: W2-W3
            'wise4' -> WISE W4 mag	 -> colors: W3-W4

        If you have magnitude measurements in other bands, use the
        `custom_bandpasses` kwarg to pass these in.

        If this is None, no object information will be incorporated into the
        checkplot (kind of making it effectively useless for anything other than
        glancing at the phased light curves at various 'best' periods from the
        period-finder results).

    varinfo : dict or None
        If this is None, a blank dict of the form below will be added to the
        checkplotdict::

            {'objectisvar': None -> variability flag (None indicates unset),
             'vartags': CSV str containing variability type tags from review,
             'varisperiodic': None -> periodic variability flag (None -> unset),
             'varperiod': the period associated with the periodic variability,
             'varepoch': the epoch associated with the periodic variability}

        If you provide a dict matching this format in this kwarg, this will be
        passed unchanged to the output checkplotdict produced.

    findercmap : str or matplotlib.cm.ColorMap object
        The Colormap object to use for the finder chart image.

    finderconvolve : astropy.convolution.Kernel object or None
        If not None, the Kernel object to use for convolving the finder image.

    sigclip : float or int or sequence of two floats/ints or None
        If a single float or int, a symmetric sigma-clip will be performed using
        the number provided as the sigma-multiplier to cut out from the input
        time-series.

        If a list of two ints/floats is provided, the function will perform an
        'asymmetric' sigma-clip. The first element in this list is the sigma
        value to use for fainter flux/mag values; the second element in this
        list is the sigma value to use for brighter flux/mag values. For
        example, `sigclip=[10., 3.]`, will sigclip out greater than 10-sigma
        dimmings and greater than 3-sigma brightenings. Here the meaning of
        "dimming" and "brightening" is set by *physics* (not the magnitude
        system), which is why the `magsarefluxes` kwarg must be correctly set.

        If `sigclip` is None, no sigma-clipping will be performed, and the
        time-series (with non-finite elems removed) will be passed through to
        the output.

    normto : {'globalmedian', 'zero'} or a float
        This is specified as below::

            'globalmedian' -> norms each mag to global median of the LC column
            'zero'         -> norms each mag to zero
            a float        -> norms each mag to this specified float value.

    normmingap : float
        This defines how much the difference between consecutive measurements is
        allowed to be to consider them as parts of different timegroups. By
        default it is set to 4.0 days.

    deredden_object : bool
        If this is True, will use the 2MASS DUST service to get extinction
        coefficients in various bands, and then try to deredden the magnitudes
        and colors of the object already present in the checkplot's objectinfo
        dict.

    custom_bandpasses : dict
        This is a dict used to provide custom bandpass definitions for any
        magnitude measurements in the objectinfo dict that are not automatically
        recognized by :py:func:`astrobase.varclass.starfeatures.color_features`.

    lclistpkl : dict or str
        If this is provided, must be a dict resulting from reading a catalog
        produced by the `lcproc.catalogs.make_lclist` function or a str path
        pointing to the pickle file produced by that function. This catalog is
        used to find neighbors of the current object in the current light curve
        collection. Looking at neighbors of the object within the radius
        specified by `nbrradiusarcsec` is useful for light curves produced by
        instruments that have a large pixel scale, so are susceptible to
        blending of variability and potential confusion of neighbor variability
        with that of the actual object being looked at. If this is None, no
        neighbor lookups will be performed.

    nbrradiusarcsec : float
        The radius in arcseconds to use for a search conducted around the
        coordinates of this object to look for any potential confusion and
        blending of variability amplitude caused by their proximity.

    maxnumneighbors : int
        The maximum number of neighbors that will have their light curves and
        magnitudes noted in this checkplot as potential blends with the target
        object.

    plotdpi : int
        The resolution in DPI of the plots to generate in this function
        (e.g. the finder chart, etc.)

    findercachedir : str
        The path to the astrobase cache directory for finder chart downloads
        from the NASA SkyView service.

    verbose : bool
        If True, will indicate progress and warn about potential problems.

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

    fast_mode : bool or float
        This runs the external catalog operations in a "fast" mode, with short
        timeouts and not trying to hit external catalogs that take a long time
        to respond.

        If this is set to True, the default settings for the external requests
        will then become::

            skyview_lookup = False
            skyview_timeout = 10.0
            skyview_retry_failed = False
            dust_timeout = 10.0
            gaia_submit_timeout = 7.0
            gaia_max_timeout = 10.0
            gaia_submit_tries = 2
            complete_query_later = False
            search_simbad = False

        If this is a float, will run in "fast" mode with the provided timeout
        value in seconds and the following settings::

            skyview_lookup = True
            skyview_timeout = fast_mode
            skyview_retry_failed = False
            dust_timeout = fast_mode
            gaia_submit_timeout = 0.66*fast_mode
            gaia_max_timeout = fast_mode
            gaia_submit_tries = 2
            complete_query_later = False
            search_simbad = False

    complete_query_later : bool
        If this is True, saves the state of GAIA queries that are not yet
        complete when `gaia_max_timeout` is reached while waiting for the GAIA
        service to respond to our request. A later call for GAIA info on the
        same object will attempt to pick up the results from the existing query
        if it's completed. If `fast_mode` is True, this is ignored.

    Returns
    -------

    dict
        A checkplotdict is returned containing the objectinfo and varinfo dicts,
        ready to use with the functions below to add in light curve plots,
        phased LC plots, xmatch info, etc.

    '''

    # optional mode to hit external services and fail fast if they timeout
    if fast_mode is True:
        skyview_lookup = False
        skyview_timeout = 10.0
        skyview_retry_failed = False
        dust_timeout = 10.0
        gaia_submit_timeout = 7.0
        gaia_max_timeout = 10.0
        gaia_submit_tries = 2
        complete_query_later = False
        search_simbad = False

    elif isinstance(fast_mode, (int, float)) and fast_mode > 0.0:
        skyview_lookup = True
        skyview_timeout = fast_mode
        skyview_retry_failed = False
        dust_timeout = fast_mode
        gaia_submit_timeout = 0.66*fast_mode
        gaia_max_timeout = fast_mode
        gaia_submit_tries = 2
        complete_query_later = False
        search_simbad = False

    else:
        skyview_lookup = True
        skyview_timeout = 10.0
        skyview_retry_failed = True
        dust_timeout = 10.0
        search_simbad = True


    if (isinstance(objectinfo, dict) and
        ('objectid' in objectinfo or 'hatid' in objectinfo) and
        'ra' in objectinfo and 'decl' in objectinfo and
        objectinfo['ra'] and objectinfo['decl']):

        if 'objectid' not in objectinfo:
            objectid = objectinfo['hatid']
        else:
            objectid = objectinfo['objectid']

        if verbose and skyview_lookup:
            LOGINFO('adding in object information and '
                    'finder chart for %s at RA: %.3f, DEC: %.3f' %
                    (objectid, objectinfo['ra'], objectinfo['decl']))
        elif verbose and not skyview_lookup:
            LOGINFO('adding in object information '
                    'for %s at RA: %.3f, DEC: %.3f. '
                    'skipping finder chart because skyview_lookup = False' %
                    (objectid, objectinfo['ra'], objectinfo['decl']))

        # get the finder chart
        try:

            if skyview_lookup:

                try:

                    # generate the finder chart
                    finder, finderheader = skyview_stamp(
                        objectinfo['ra'],
                        objectinfo['decl'],
                        convolvewith=finderconvolve,
                        verbose=verbose,
                        flip=False,
                        cachedir=findercachedir,
                        timeout=skyview_timeout,
                        retry_failed=skyview_retry_failed,
                    )

                except OSError as e:

                    if not fast_mode:

                        LOGERROR(
                            'finder image appears to be corrupt, retrying...'
                        )

                        # generate the finder chart
                        finder, finderheader = skyview_stamp(
                            objectinfo['ra'],
                            objectinfo['decl'],
                            convolvewith=finderconvolve,
                            verbose=verbose,
                            flip=False,
                            cachedir=findercachedir,
                            forcefetch=True,
                            timeout=skyview_timeout,
                            retry_failed=False  # do not start an infinite loop
                        )


                finderfig = plt.figure(figsize=(3,3),dpi=plotdpi)

                # initialize the finder WCS
                finderwcs = WCS(finderheader)

                # use the WCS transform for the plot
                ax = finderfig.add_subplot(111, frameon=False)
                ax.imshow(finder, cmap=findercmap, origin='lower')

            else:
                finder, finderheader, finderfig, finderwcs = (
                    None, None, None, None
                )

            # skip down to after nbr stuff for the rest of the finderchart...

            # search around the target's location and get its neighbors if
            # lclistpkl is provided and it exists
            if (lclistpkl is not None and
                nbrradiusarcsec is not None and
                nbrradiusarcsec > 0.0):

                # if lclistpkl is a string, open it as a pickle
                if isinstance(lclistpkl, str) and os.path.exists(lclistpkl):

                    if lclistpkl.endswith('.gz'):
                        infd = gzip.open(lclistpkl,'rb')
                    else:
                        infd = open(lclistpkl,'rb')

                    lclist = pickle.load(infd)
                    infd.close()

                # otherwise, if it's a dict, we get it directly
                elif isinstance(lclistpkl, dict):

                    lclist = lclistpkl

                # finally, if it's nothing we recognize, ignore it
                else:

                    LOGERROR('could not understand lclistpkl kwarg, '
                             'not getting neighbor info')

                    lclist = dict()

                # check if we have a KDTree to use
                # if we don't, skip neighbor stuff
                if 'kdtree' not in lclist:

                    LOGERROR('neighbors within %.1f arcsec for %s could '
                             'not be found, no kdtree in lclistpkl: %s'
                             % (objectid, lclistpkl))
                    neighbors = None
                    kdt = None

                # otherwise, do neighbor processing
                else:

                    kdt = lclist['kdtree']

                    obj_cosdecl = np.cos(np.radians(objectinfo['decl']))
                    obj_sindecl = np.sin(np.radians(objectinfo['decl']))
                    obj_cosra = np.cos(np.radians(objectinfo['ra']))
                    obj_sinra = np.sin(np.radians(objectinfo['ra']))

                    obj_xyz = np.column_stack((obj_cosra*obj_cosdecl,
                                               obj_sinra*obj_cosdecl,
                                               obj_sindecl))
                    match_xyzdist = (
                        2.0 * np.sin(np.radians(nbrradiusarcsec/3600.0)/2.0)
                    )
                    matchdists, matchinds = kdt.query(
                        obj_xyz,
                        k=maxnumneighbors+1,  # get maxnumneighbors + tgt
                        distance_upper_bound=match_xyzdist
                    )

                    # sort by matchdist
                    mdsorted = np.argsort(matchdists[0])
                    matchdists = matchdists[0][mdsorted]
                    matchinds = matchinds[0][mdsorted]

                    # luckily, the indices to the kdtree are the same as that
                    # for the objects (I think)
                    neighbors = []

                    nbrind = 0

                    for md, mi in zip(matchdists, matchinds):

                        if np.isfinite(md) and md > 0.0:

                            if skyview_lookup:

                                # generate the xy for the finder we'll use a
                                # HTML5 canvas and these pixcoords to highlight
                                # each neighbor when we mouse over its row in
                                # the neighbors tab

                                # we use coord origin = 0 here and not the usual
                                # 1 because we're annotating a numpy array
                                pixcoords = finderwcs.all_world2pix(
                                    np.array([[lclist['objects']['ra'][mi],
                                               lclist['objects']['decl'][mi]]]),
                                    0
                                )

                                # each elem is {'objectid',
                                #               'ra','decl',
                                #               'xpix','ypix',
                                #               'dist','lcfpath'}
                                thisnbr = {
                                    'objectid':(
                                        lclist['objects']['objectid'][mi]
                                    ),
                                    'ra':lclist['objects']['ra'][mi],
                                    'decl':lclist['objects']['decl'][mi],
                                    'xpix':pixcoords[0,0],
                                    'ypix':300.0 - pixcoords[0,1],
                                    'dist':_xyzdist_to_distarcsec(md),
                                    'lcfpath': lclist['objects']['lcfname'][mi]
                                }
                                neighbors.append(thisnbr)
                                nbrind = nbrind+1

                                # put in a nice marker for this neighbor into
                                # the overall finder chart
                                annotatex = pixcoords[0,0]
                                annotatey = pixcoords[0,1]

                                if ((300.0 - annotatex) > 50.0):
                                    offx = annotatex + 30.0
                                    xha = 'center'
                                else:
                                    offx = annotatex - 30.0
                                    xha = 'center'
                                if ((300.0 - annotatey) > 50.0):
                                    offy = annotatey - 30.0
                                    yha = 'center'
                                else:
                                    offy = annotatey + 30.0
                                    yha = 'center'

                                ax.annotate('N%s' % nbrind,
                                            (annotatex, annotatey),
                                            xytext=(offx, offy),
                                            arrowprops={'facecolor':'blue',
                                                        'edgecolor':'blue',
                                                        'width':1.0,
                                                        'headwidth':1.0,
                                                        'headlength':0.1,
                                                        'shrink':0.0},
                                            color='blue',
                                            horizontalalignment=xha,
                                            verticalalignment=yha)

                            else:

                                thisnbr = {
                                    'objectid':(
                                        lclist['objects']['objectid'][mi]
                                    ),
                                    'ra':lclist['objects']['ra'][mi],
                                    'decl':lclist['objects']['decl'][mi],
                                    'xpix':0.0,
                                    'ypix':0.0,
                                    'dist':_xyzdist_to_distarcsec(md),
                                    'lcfpath': lclist['objects']['lcfname'][mi]
                                }
                                neighbors.append(thisnbr)
                                nbrind = nbrind+1

            # if there are no neighbors, set the 'neighbors' key to None
            else:

                neighbors = None
                kdt = None

            if skyview_lookup:

                #
                # finish up the finder chart after neighbors are processed
                #
                ax.set_xticks([])
                ax.set_yticks([])

                # add a reticle pointing to the object's coordinates
                # we use coord origin = 0 here and not the usual
                # 1 because we're annotating a numpy array
                object_pixcoords = finderwcs.all_world2pix(
                    [[objectinfo['ra'],
                      objectinfo['decl']]],
                    0
                )

                ax.axvline(
                    # x=150.0,
                    x=object_pixcoords[0,0],
                    ymin=0.375,
                    ymax=0.45,
                    linewidth=1,
                    color='b'
                )
                ax.axhline(
                    # y=150.0,
                    y=object_pixcoords[0,1],
                    xmin=0.375,
                    xmax=0.45,
                    linewidth=1,
                    color='b'
                )
                ax.set_frame_on(False)

                # this is the output instance
                finderpng = StrIO()
                finderfig.savefig(finderpng,
                                  bbox_inches='tight',
                                  pad_inches=0.0, format='png')
                plt.close()

                # encode the finderpng instance to base64
                finderpng.seek(0)
                finderb64 = base64.b64encode(finderpng.read())

                # close the stringio buffer
                finderpng.close()

            else:

                finderb64 = None

        except Exception as e:

            LOGEXCEPTION('could not fetch a DSS stamp for this '
                         'object %s using coords (%.3f,%.3f)' %
                         (objectid, objectinfo['ra'], objectinfo['decl']))
            finderb64 = None
            neighbors = None
            kdt = None

    # if we don't have ra, dec info, then everything is none up to this point
    else:

        finderb64 = None
        neighbors = None
        kdt = None

    #
    # end of finder chart operations
    #

    # now that we have the finder chart, get the rest of the object
    # information

    # get the rest of the features, these don't necessarily rely on ra, dec and
    # should degrade gracefully if these aren't provided
    if isinstance(objectinfo, dict):

        if 'objectid' not in objectinfo and 'hatid' in objectinfo:
            objectid = objectinfo['hatid']
            objectinfo['objectid'] = objectid
        elif 'objectid' in objectinfo:
            objectid = objectinfo['objectid']
        else:
            objectid = os.urandom(12).hex()[:7]
            objectinfo['objectid'] = objectid
            LOGWARNING('no objectid found in objectinfo dict, '
                       'making up a random one: %s')


        # get the neighbor features and GAIA info
        nbrfeat = neighbor_gaia_features(
            objectinfo,
            kdt,
            nbrradiusarcsec,
            verbose=False,
            gaia_submit_timeout=gaia_submit_timeout,
            gaia_submit_tries=gaia_submit_tries,
            gaia_max_timeout=gaia_max_timeout,
            gaia_mirror=gaia_mirror,
            complete_query_later=complete_query_later,
            search_simbad=search_simbad
        )
        objectinfo.update(nbrfeat)

        # see if the objectinfo dict has pmra/pmdecl entries.  if it doesn't,
        # then we'll see if the nbrfeat dict has pmra/pmdecl from GAIA. we'll
        # set the appropriate provenance keys as well so we know where the PM
        # came from
        if ( ('pmra' not in objectinfo) or
             ( ('pmra' in objectinfo) and
               ( (objectinfo['pmra'] is None) or
                 (not np.isfinite(objectinfo['pmra'])) ) ) ):

            if 'ok' in nbrfeat['gaia_status']:

                objectinfo['pmra'] = nbrfeat['gaia_pmras'][0]
                objectinfo['pmra_err'] = nbrfeat['gaia_pmra_errs'][0]
                objectinfo['pmra_source'] = 'gaia'

                if verbose:
                    LOGWARNING('pmRA not found in provided objectinfo dict, '
                               'using value from GAIA')

        else:
            objectinfo['pmra_source'] = 'light curve'

        if ( ('pmdecl' not in objectinfo) or
             ( ('pmdecl' in objectinfo) and
               ( (objectinfo['pmdecl'] is None) or
                 (not np.isfinite(objectinfo['pmdecl'])) ) ) ):

            if 'ok' in nbrfeat['gaia_status']:

                objectinfo['pmdecl'] = nbrfeat['gaia_pmdecls'][0]
                objectinfo['pmdecl_err'] = nbrfeat['gaia_pmdecl_errs'][0]
                objectinfo['pmdecl_source'] = 'gaia'

                if verbose:
                    LOGWARNING('pmDEC not found in provided objectinfo dict, '
                               'using value from GAIA')

        else:
            objectinfo['pmdecl_source'] = 'light curve'

        #
        # update GAIA info so it's available at the first level
        #
        if 'ok' in objectinfo['gaia_status']:
            objectinfo['gaiaid'] = objectinfo['gaia_ids'][0]
            objectinfo['gaiamag'] = objectinfo['gaia_mags'][0]
            objectinfo['gaia_absmag'] = objectinfo['gaia_absolute_mags'][0]
            objectinfo['gaia_parallax'] = objectinfo['gaia_parallaxes'][0]
            objectinfo['gaia_parallax_err'] = (
                objectinfo['gaia_parallax_errs'][0]
            )
            objectinfo['gaia_pmra'] = objectinfo['gaia_pmras'][0]
            objectinfo['gaia_pmra_err'] = objectinfo['gaia_pmra_errs'][0]
            objectinfo['gaia_pmdecl'] = objectinfo['gaia_pmdecls'][0]
            objectinfo['gaia_pmdecl_err'] = objectinfo['gaia_pmdecl_errs'][0]

        else:
            objectinfo['gaiaid'] = None
            objectinfo['gaiamag'] = np.nan
            objectinfo['gaia_absmag'] = np.nan
            objectinfo['gaia_parallax'] = np.nan
            objectinfo['gaia_parallax_err'] = np.nan
            objectinfo['gaia_pmra'] = np.nan
            objectinfo['gaia_pmra_err'] = np.nan
            objectinfo['gaia_pmdecl'] = np.nan
            objectinfo['gaia_pmdecl_err'] = np.nan

        #
        # get the object's TIC information
        #
        if ('ra' in objectinfo and
            objectinfo['ra'] is not None and
            np.isfinite(objectinfo['ra']) and
            'decl' in objectinfo and
            objectinfo['decl'] is not None and
            np.isfinite(objectinfo['decl'])):

            try:
                ticres = tic_conesearch(objectinfo['ra'],
                                        objectinfo['decl'],
                                        radius_arcmin=5.0/60.0,
                                        verbose=verbose,
                                        timeout=gaia_max_timeout,
                                        maxtries=gaia_submit_tries)

                if ticres is not None:

                    with open(ticres['cachefname'],'r') as infd:
                        ticinfo = json.load(infd)

                    if ('data' in ticinfo and
                        len(ticinfo['data']) > 0 and
                        isinstance(ticinfo['data'][0], dict)):

                        objectinfo['ticid'] = str(ticinfo['data'][0]['ID'])
                        objectinfo['tessmag'] = ticinfo['data'][0]['Tmag']
                        objectinfo['tic_version'] = (
                            ticinfo['data'][0]['version']
                        )
                        objectinfo['tic_distarcsec'] = (
                            ticinfo['data'][0]['dstArcSec']
                        )
                        objectinfo['tessmag_origin'] = (
                            ticinfo['data'][0]['TESSflag']
                        )

                        objectinfo['tic_starprop_origin'] = (
                            ticinfo['data'][0]['SPFlag']
                        )
                        objectinfo['tic_lumclass'] = (
                            ticinfo['data'][0]['lumclass']
                        )
                        objectinfo['tic_teff'] = (
                            ticinfo['data'][0]['Teff']
                        )
                        objectinfo['tic_teff_err'] = (
                            ticinfo['data'][0]['e_Teff']
                        )
                        objectinfo['tic_logg'] = (
                            ticinfo['data'][0]['logg']
                        )
                        objectinfo['tic_logg_err'] = (
                            ticinfo['data'][0]['e_logg']
                        )
                        objectinfo['tic_mh'] = (
                            ticinfo['data'][0]['MH']
                        )
                        objectinfo['tic_mh_err'] = (
                            ticinfo['data'][0]['e_MH']
                        )
                        objectinfo['tic_radius'] = (
                            ticinfo['data'][0]['rad']
                        )
                        objectinfo['tic_radius_err'] = (
                            ticinfo['data'][0]['e_rad']
                        )
                        objectinfo['tic_mass'] = (
                            ticinfo['data'][0]['mass']
                        )
                        objectinfo['tic_mass_err'] = (
                            ticinfo['data'][0]['e_mass']
                        )
                        objectinfo['tic_density'] = (
                            ticinfo['data'][0]['rho']
                        )
                        objectinfo['tic_density_err'] = (
                            ticinfo['data'][0]['e_rho']
                        )
                        objectinfo['tic_luminosity'] = (
                            ticinfo['data'][0]['lum']
                        )
                        objectinfo['tic_luminosity_err'] = (
                            ticinfo['data'][0]['e_lum']
                        )
                        objectinfo['tic_distancepc'] = (
                            ticinfo['data'][0]['d']
                        )
                        objectinfo['tic_distancepc_err'] = (
                            ticinfo['data'][0]['e_d']
                        )

                        #
                        # fill in any missing info using the TIC entry
                        #
                        if ('gaiaid' not in objectinfo or
                            ('gaiaid' in objectinfo and
                             (objectinfo['gaiaid'] is None))):
                            objectinfo['gaiaid'] = ticinfo['data'][0]['GAIA']

                        if ('gaiamag' not in objectinfo or
                            ('gaiamag' in objectinfo and
                             (objectinfo['gaiamag'] is None or
                              not np.isfinite(objectinfo['gaiamag'])))):
                            objectinfo['gaiamag'] = (
                                ticinfo['data'][0]['GAIAmag']
                            )
                            objectinfo['gaiamag_err'] = (
                                ticinfo['data'][0]['e_GAIAmag']
                            )

                        if ('gaia_parallax' not in objectinfo or
                            ('gaia_parallax' in objectinfo and
                             (objectinfo['gaia_parallax'] is None or
                              not np.isfinite(objectinfo['gaia_parallax'])))):

                            objectinfo['gaia_parallax'] = (
                                ticinfo['data'][0]['plx']
                            )
                            objectinfo['gaia_parallax_err'] = (
                                ticinfo['data'][0]['e_plx']
                            )

                            if (objectinfo['gaiamag'] is not None and
                                np.isfinite(objectinfo['gaiamag']) and
                                objectinfo['gaia_parallax'] is not None and
                                np.isfinite(objectinfo['gaia_parallax'])):

                                objectinfo['gaia_absmag'] = (
                                    magnitudes.absolute_gaia_magnitude(
                                        objectinfo['gaiamag'],
                                        objectinfo['gaia_parallax']
                                    )
                                )

                        if ('pmra' not in objectinfo or
                            ('pmra' in objectinfo and
                             (objectinfo['pmra'] is None or
                              not np.isfinite(objectinfo['pmra'])))):
                            objectinfo['pmra'] = ticinfo['data'][0]['pmRA']
                            objectinfo['pmra_err'] = (
                                ticinfo['data'][0]['e_pmRA']
                            )
                            objectinfo['pmra_source'] = 'TIC'

                        if ('pmdecl' not in objectinfo or
                            ('pmdecl' in objectinfo and
                             (objectinfo['pmdecl'] is None or
                              not np.isfinite(objectinfo['pmdecl'])))):
                            objectinfo['pmdecl'] = ticinfo['data'][0]['pmDEC']
                            objectinfo['pmdecl_err'] = (
                                ticinfo['data'][0]['e_pmDEC']
                            )
                            objectinfo['pmdecl_source'] = 'TIC'

                        if ('bmag' not in objectinfo or
                            ('bmag' in objectinfo and
                             (objectinfo['bmag'] is None or
                              not np.isfinite(objectinfo['bmag'])))):
                            objectinfo['bmag'] = ticinfo['data'][0]['Bmag']
                            objectinfo['bmag_err'] = (
                                ticinfo['data'][0]['e_Bmag']
                            )

                        if ('vmag' not in objectinfo or
                            ('vmag' in objectinfo and
                             (objectinfo['vmag'] is None or
                              not np.isfinite(objectinfo['vmag'])))):
                            objectinfo['vmag'] = ticinfo['data'][0]['Vmag']
                            objectinfo['vmag_err'] = (
                                ticinfo['data'][0]['e_Vmag']
                            )

                        if ('sdssu' not in objectinfo or
                            ('sdssu' in objectinfo and
                             (objectinfo['sdssu'] is None or
                              not np.isfinite(objectinfo['sdssu'])))):
                            objectinfo['sdssu'] = ticinfo['data'][0]['umag']
                            objectinfo['sdssu_err'] = (
                                ticinfo['data'][0]['e_umag']
                            )

                        if ('sdssg' not in objectinfo or
                            ('sdssg' in objectinfo and
                             (objectinfo['sdssg'] is None or
                              not np.isfinite(objectinfo['sdssg'])))):
                            objectinfo['sdssg'] = ticinfo['data'][0]['gmag']
                            objectinfo['sdssg_err'] = (
                                ticinfo['data'][0]['e_gmag']
                            )

                        if ('sdssr' not in objectinfo or
                            ('sdssr' in objectinfo and
                             (objectinfo['sdssr'] is None or
                              not np.isfinite(objectinfo['sdssr'])))):
                            objectinfo['sdssr'] = ticinfo['data'][0]['rmag']
                            objectinfo['sdssr_err'] = (
                                ticinfo['data'][0]['e_rmag']
                            )

                        if ('sdssi' not in objectinfo or
                            ('sdssi' in objectinfo and
                             (objectinfo['sdssi'] is None or
                              not np.isfinite(objectinfo['sdssi'])))):
                            objectinfo['sdssi'] = ticinfo['data'][0]['imag']
                            objectinfo['sdssi_err'] = (
                                ticinfo['data'][0]['e_imag']
                            )

                        if ('sdssz' not in objectinfo or
                            ('sdssz' in objectinfo and
                             (objectinfo['sdssz'] is None or
                              not np.isfinite(objectinfo['sdssz'])))):
                            objectinfo['sdssz'] = ticinfo['data'][0]['zmag']
                            objectinfo['sdssz_err'] = (
                                ticinfo['data'][0]['e_zmag']
                            )

                        if ('jmag' not in objectinfo or
                            ('jmag' in objectinfo and
                             (objectinfo['jmag'] is None or
                              not np.isfinite(objectinfo['jmag'])))):
                            objectinfo['jmag'] = ticinfo['data'][0]['Jmag']
                            objectinfo['jmag_err'] = (
                                ticinfo['data'][0]['e_Jmag']
                            )

                        if ('hmag' not in objectinfo or
                            ('hmag' in objectinfo and
                             (objectinfo['hmag'] is None or
                              not np.isfinite(objectinfo['hmag'])))):
                            objectinfo['hmag'] = ticinfo['data'][0]['Hmag']
                            objectinfo['hmag_err'] = (
                                ticinfo['data'][0]['e_Hmag']
                            )

                        if ('kmag' not in objectinfo or
                            ('kmag' in objectinfo and
                             (objectinfo['kmag'] is None or
                              not np.isfinite(objectinfo['kmag'])))):
                            objectinfo['kmag'] = ticinfo['data'][0]['Kmag']
                            objectinfo['kmag_err'] = (
                                ticinfo['data'][0]['e_Kmag']
                            )

                        if ('wise1' not in objectinfo or
                            ('wise1' in objectinfo and
                             (objectinfo['wise1'] is None or
                              not np.isfinite(objectinfo['wise1'])))):
                            objectinfo['wise1'] = ticinfo['data'][0]['w1mag']
                            objectinfo['wise1_err'] = (
                                ticinfo['data'][0]['e_w1mag']
                            )

                        if ('wise2' not in objectinfo or
                            ('wise2' in objectinfo and
                             (objectinfo['wise2'] is None or
                              not np.isfinite(objectinfo['wise2'])))):
                            objectinfo['wise2'] = ticinfo['data'][0]['w2mag']
                            objectinfo['wise2_err'] = (
                                ticinfo['data'][0]['e_w2mag']
                            )

                        if ('wise3' not in objectinfo or
                            ('wise3' in objectinfo and
                             (objectinfo['wise3'] is None or
                              not np.isfinite(objectinfo['wise3'])))):
                            objectinfo['wise3'] = ticinfo['data'][0]['w3mag']
                            objectinfo['wise3_err'] = (
                                ticinfo['data'][0]['e_w3mag']
                            )

                        if ('wise4' not in objectinfo or
                            ('wise4' in objectinfo and
                             (objectinfo['wise4'] is None or
                              not np.isfinite(objectinfo['wise4'])))):
                            objectinfo['wise4'] = ticinfo['data'][0]['w4mag']
                            objectinfo['wise4_err'] = (
                                ticinfo['data'][0]['e_w4mag']
                            )

                else:
                    LOGERROR('could not look up TIC '
                             'information for object: %s '
                             'at (%.3f, %.3f)' %
                             (objectinfo['objectid'],
                              objectinfo['ra'],
                              objectinfo['decl']))

            except Exception as e:

                LOGEXCEPTION('could not look up TIC '
                             'information for object: %s '
                             'at (%.3f, %.3f)' %
                             (objectinfo['objectid'],
                              objectinfo['ra'],
                              objectinfo['decl']))


        # try to get the object's coord features
        coordfeat = coord_features(objectinfo)

        # get the color features
        colorfeat = color_features(objectinfo,
                                   deredden=deredden_object,
                                   custom_bandpasses=custom_bandpasses,
                                   dust_timeout=dust_timeout)

        # get the object's color classification
        colorclass = color_classification(colorfeat, coordfeat)

        # update the objectinfo dict with everything
        objectinfo.update(colorfeat)
        objectinfo.update(coordfeat)
        objectinfo.update(colorclass)

        # put together the initial checkplot pickle dictionary
        # this will be updated by the functions below as appropriate
        # and will written out as a gzipped pickle at the end of processing
        checkplotdict = {'objectid':objectid,
                         'neighbors':neighbors,
                         'objectinfo':objectinfo,
                         'finderchart':finderb64,
                         'sigclip':sigclip,
                         'normto':normto,
                         'normmingap':normmingap}

        # add the objecttags key to objectinfo
        checkplotdict['objectinfo']['objecttags'] = None

    # if there's no objectinfo, we can't do anything.
    else:

        # empty objectinfo dict
        checkplotdict = {'objectid':None,
                         'neighbors':None,
                         'objectinfo':{
                             'available_bands':[],
                             'available_band_labels':[],
                             'available_dereddened_bands':[],
                             'available_dereddened_band_labels':[],
                             'available_colors':[],
                             'available_color_labels':[],
                             'bmag':None,
                             'bmag-vmag':None,
                             'decl':None,
                             'hatid':None,
                             'hmag':None,
                             'imag-jmag':None,
                             'jmag-kmag':None,
                             'jmag':None,
                             'kmag':None,
                             'ndet':None,
                             'network':None,
                             'objecttags':None,
                             'pmdecl':None,
                             'pmdecl_err':None,
                             'pmra':None,
                             'pmra_err':None,
                             'propermotion':None,
                             'ra':None,
                             'rpmj':None,
                             'sdssg':None,
                             'sdssi':None,
                             'sdssr':None,
                             'stations':None,
                             'twomassid':None,
                             'ucac4id':None,
                             'vmag':None
                         },
                         'finderchart':None,
                         'sigclip':sigclip,
                         'normto':normto,
                         'normmingap':normmingap}

    # end of objectinfo processing

    # add the varinfo dict
    if isinstance(varinfo, dict):
        checkplotdict['varinfo'] = varinfo
    else:
        checkplotdict['varinfo'] = {
            'objectisvar':None,
            'vartags':None,
            'varisperiodic':None,
            'varperiod':None,
            'varepoch':None,
        }

    return checkplotdict