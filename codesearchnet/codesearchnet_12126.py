def query_radecl(ra,
                 decl,
                 filtersystem='sloan_2mass',
                 field_deg2=1.0,
                 usebinaries=True,
                 extinction_sigma=0.1,
                 magnitude_limit=26.0,
                 maglim_filtercol=4,
                 trilegal_version=1.6,
                 extraparams=None,
                 forcefetch=False,
                 cachedir='~/.astrobase/trilegal-cache',
                 verbose=True,
                 timeout=60.0,
                 refresh=150.0,
                 maxtimeout=700.0):
    '''This runs the TRILEGAL query for decimal equatorial coordinates.

    Parameters
    ----------

    ra,decl : float
        These are the center equatorial coordinates in decimal degrees

    filtersystem : str
        This is a key in the TRILEGAL_FILTER_SYSTEMS dict. Use the function
        :py:func:`astrobase.services.trilegal.list_trilegal_filtersystems` to
        see a nicely formatted table with the key and description for each of
        these.

    field_deg2 : float
        The area of the simulated field in square degrees. This is in the
        Galactic coordinate system.

    usebinaries : bool
        If this is True, binaries will be present in the model results.

    extinction_sigma : float
        This is the applied std dev around the `Av_extinction` value for the
        galactic coordinates requested.

    magnitude_limit : float
        This is the limiting magnitude of the simulation in the
        `maglim_filtercol` band index of the filter system chosen.

    maglim_filtercol : int
        The index in the filter system list of the magnitude limiting band.

    trilegal_version : float
        This is the the version of the TRILEGAL form to use. This can usually be
        left as-is.

    extraparams : dict or None
        This is a dict that can be used to override parameters of the model
        other than the basic ones used for input to this function. All
        parameters are listed in `TRILEGAL_DEFAULT_PARAMS` above. See:

        http://stev.oapd.inaf.it/cgi-bin/trilegal

        for explanations of these parameters.

    forcefetch : bool
        If this is True, the query will be retried even if cached results for
        it exist.

    cachedir : str
        This points to the directory where results will be downloaded.

    verbose : bool
        If True, will indicate progress and warn of any issues.

    timeout : float
        This sets the amount of time in seconds to wait for the service to
        respond to our initial request.

    refresh : float
        This sets the amount of time in seconds to wait before checking if the
        result file is available. If the results file isn't available after
        `refresh` seconds have elapsed, the function will wait for `refresh`
        seconds continuously, until `maxtimeout` is reached or the results file
        becomes available.

    maxtimeout : float
        The maximum amount of time in seconds to wait for a result to become
        available after submitting our query request.

    Returns
    -------

    dict
        This returns a dict of the form::

            {'params':the input param dict used,
             'extraparams':any extra params used,
             'provenance':'cached' or 'new download',
             'tablefile':the path on disk to the downloaded model text file}

    '''

    # convert the ra/decl to gl, gb
    radecl = SkyCoord(ra=ra*u.degree, dec=decl*u.degree)

    gl = radecl.galactic.l.degree
    gb = radecl.galactic.b.degree

    return query_galcoords(gl,
                           gb,
                           filtersystem=filtersystem,
                           field_deg2=field_deg2,
                           usebinaries=usebinaries,
                           extinction_sigma=extinction_sigma,
                           magnitude_limit=magnitude_limit,
                           maglim_filtercol=maglim_filtercol,
                           trilegal_version=trilegal_version,
                           extraparams=extraparams,
                           forcefetch=forcefetch,
                           cachedir=cachedir,
                           verbose=verbose,
                           timeout=timeout,
                           refresh=refresh,
                           maxtimeout=maxtimeout)