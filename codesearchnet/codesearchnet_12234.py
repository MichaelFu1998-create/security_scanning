def objectlist_conesearch(racenter,
                          declcenter,
                          searchradiusarcsec,
                          gaia_mirror=None,
                          columns=('source_id',
                                   'ra','dec',
                                   'phot_g_mean_mag',
                                   'l','b',
                                   'parallax', 'parallax_error',
                                   'pmra','pmra_error',
                                   'pmdec','pmdec_error'),
                          extra_filter=None,
                          returnformat='csv',
                          forcefetch=False,
                          cachedir='~/.astrobase/gaia-cache',
                          verbose=True,
                          timeout=15.0,
                          refresh=2.0,
                          maxtimeout=300.0,
                          maxtries=3,
                          complete_query_later=True):
    '''This queries the GAIA TAP service for a list of objects near the coords.

    Runs a conesearch around `(racenter, declcenter)` with radius in arcsec of
    `searchradiusarcsec`.

    Parameters
    ----------

    racenter,declcenter : float
        The center equatorial coordinates in decimal degrees.

    searchradiusarcsec : float
        The search radius of the cone-search in arcseconds.

    gaia_mirror : {'gaia','heidelberg','vizier'} or None
        This is the key used to select a GAIA catalog mirror from the
        `GAIA_URLS` dict above. If set, the specified mirror will be used. If
        None, a random mirror chosen from that dict will be used.

    columns : sequence of str
        This indicates which columns from the GAIA table to request for the
        objects found within the search radius.

    extra_filter: str or None
        If this is provided, must be a valid ADQL filter string that is used to
        further filter the cone-search results.

    returnformat : {'csv','votable','json'}
        The returned file format to request from the GAIA catalog service.

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

    maxtries : int
        The maximum number of tries (across all mirrors tried) to make to either
        submit the request or download the results, before giving up.

    completequerylater : bool
        If set to True, a submitted query that does not return a result before
        `maxtimeout` has passed will be cancelled but its input request
        parameters and the result URL provided by the service will be saved. If
        this function is then called later with these same input request
        parameters, it will check if the query finally finished and a result is
        available. If so, will download the results instead of submitting a new
        query. If it's not done yet, will start waiting for results again. To
        force launch a new query with the same request parameters, set the
        `forcefetch` kwarg to True.

    Returns
    -------

    dict
        This returns a dict of the following form::

            {'params':dict of the input params used for the query,
             'provenance':'cache' or 'new download',
             'result':path to the file on disk with the downloaded data table}

    '''

    # this was generated using the awesome query generator at:
    # https://gea.esac.esa.int/archive/

    # NOTE: here we don't resolve the table name right away. this is because
    # some of the GAIA mirrors use different table names, so we leave the table
    # name to be resolved by the lower level tap_query function. this is done by
    # the {{table}} construct.
    query = (
        "select {columns}, "
        "(DISTANCE(POINT('ICRS', "
        "{{table}}.ra, {{table}}.dec), "
        "POINT('ICRS', {ra_center:.5f}, {decl_center:.5f})))*3600.0 "
        "AS dist_arcsec "
        "from {{table}} where "
        "CONTAINS(POINT('ICRS',{{table}}.ra, {{table}}.dec),"
        "CIRCLE('ICRS',{ra_center:.5f},{decl_center:.5f},"
        "{search_radius:.6f}))=1 "
        "{extra_filter_str}"
        "ORDER by dist_arcsec asc "
    )

    if extra_filter is not None:
        extra_filter_str = ' and %s ' % extra_filter
    else:
        extra_filter_str = ''

    formatted_query = query.format(ra_center=racenter,
                                   decl_center=declcenter,
                                   search_radius=searchradiusarcsec/3600.0,
                                   extra_filter_str=extra_filter_str,
                                   columns=', '.join(columns))

    return tap_query(formatted_query,
                     gaia_mirror=gaia_mirror,
                     returnformat=returnformat,
                     forcefetch=forcefetch,
                     cachedir=cachedir,
                     verbose=verbose,
                     timeout=timeout,
                     refresh=refresh,
                     maxtimeout=maxtimeout,
                     maxtries=maxtries,
                     complete_query_later=complete_query_later)