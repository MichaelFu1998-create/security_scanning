def objectlist_radeclbox(radeclbox,
                         gaia_mirror=None,
                         columns=('source_id',
                                  'ra','dec',
                                  'phot_g_mean_mag',
                                  'l','b',
                                  'parallax, parallax_error',
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

    '''This queries the GAIA TAP service for a list of objects in an equatorial
    coordinate box.

    Parameters
    ----------

    radeclbox : sequence of four floats
        This defines the box to search in::

            [ra_min, ra_max, decl_min, decl_max]

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
        "select {columns} from {{table}} where "
        "CONTAINS(POINT('ICRS',{{table}}.ra, {{table}}.dec),"
        "BOX('ICRS',{ra_center:.5f},{decl_center:.5f},"
        "{ra_width:.5f},{decl_height:.5f}))=1"
        "{extra_filter_str}"
    )

    ra_min, ra_max, decl_min, decl_max = radeclbox
    ra_center = (ra_max + ra_min)/2.0
    decl_center = (decl_max + decl_min)/2.0
    ra_width = ra_max - ra_min
    decl_height = decl_max - decl_min

    if extra_filter is not None:
        extra_filter_str = ' and %s ' % extra_filter
    else:
        extra_filter_str = ''

    formatted_query = query.format(columns=', '.join(columns),
                                   extra_filter_str=extra_filter_str,
                                   ra_center=ra_center,
                                   decl_center=decl_center,
                                   ra_width=ra_width,
                                   decl_height=decl_height)

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