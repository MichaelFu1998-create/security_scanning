def objectnames_conesearch(racenter,
                           declcenter,
                           searchradiusarcsec,
                           simbad_mirror='simbad',
                           returnformat='csv',
                           forcefetch=False,
                           cachedir='~/.astrobase/simbad-cache',
                           verbose=True,
                           timeout=10.0,
                           refresh=2.0,
                           maxtimeout=90.0,
                           maxtries=1,
                           complete_query_later=True):
    '''This queries the SIMBAD TAP service for a list of object names near the
    coords. This is effectively a "reverse" name resolver (i.e. this does the
    opposite of SESAME).

    Parameters
    ----------

    racenter,declcenter : float
        The cone-search center coordinates in decimal degrees

    searchradiusarcsec : float
        The radius in arcseconds to search around the center coordinates.

    simbad_mirror : str
        This is the key used to select a SIMBAD mirror from the
        `SIMBAD_URLS` dict above. If set, the specified mirror will be used. If
        None, a random mirror chosen from that dict will be used.

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

    complete_query_later : bool
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

    # this was generated using the example at:
    # http://simbad.u-strasbg.fr/simbad/sim-tap and the table diagram at:
    # http://simbad.u-strasbg.fr/simbad/tap/tapsearch.html
    query = (
        "select a.oid, a.ra, a.dec, a.main_id, a.otype_txt, "
        "a.coo_bibcode, a.nbref, b.ids as all_ids, "
        "(DISTANCE(POINT('ICRS', a.ra, a.dec), "
        "POINT('ICRS', {ra_center:.5f}, {decl_center:.5f})))*3600.0 "
        "AS dist_arcsec "
        "from basic a join ids b on a.oid = b.oidref where "
        "CONTAINS(POINT('ICRS',a.ra, a.dec),"
        "CIRCLE('ICRS',{ra_center:.5f},{decl_center:.5f},"
        "{search_radius:.6f}))=1 "
        "ORDER by dist_arcsec asc "
    )

    formatted_query = query.format(ra_center=racenter,
                                   decl_center=declcenter,
                                   search_radius=searchradiusarcsec/3600.0)

    return tap_query(formatted_query,
                     simbad_mirror=simbad_mirror,
                     returnformat=returnformat,
                     forcefetch=forcefetch,
                     cachedir=cachedir,
                     verbose=verbose,
                     timeout=timeout,
                     refresh=refresh,
                     maxtimeout=maxtimeout,
                     maxtries=maxtries,
                     complete_query_later=complete_query_later)