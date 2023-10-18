def tic_objectsearch(
        objectid,
        idcol_to_use="ID",
        apiversion='v0',
        forcefetch=False,
        cachedir='~/.astrobase/mast-cache',
        verbose=True,
        timeout=90.0,
        refresh=5.0,
        maxtimeout=180.0,
        maxtries=3,
        jitter=5.0,
        raiseonfail=False
):
    '''
    This runs a TIC search for a specified TIC ID.

    Parameters
    ----------

    objectid : str
        The object ID to look up information for.

    idcol_to_use : str
        This is the name of the object ID column to use when looking up the
        provided `objectid`. This is one of {'ID', 'HIP', 'TYC', 'UCAC',
        'TWOMASS', 'ALLWISE', 'SDSS', 'GAIA', 'APASS', 'KIC'}.

    apiversion : str
        The API version of the MAST service to use. This sets the URL that this
        function will call, using `apiversion` as key into the `MAST_URLS` dict
        above.

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

    jitter : float
        This is used to control the scale of the random wait in seconds before
        starting the query. Useful in parallelized situations.

    raiseonfail : bool
        If this is True, the function will raise an Exception if something goes
        wrong, instead of returning None.

    Returns
    -------

    dict
        This returns a dict of the following form::

            {'params':dict of the input params used for the query,
             'provenance':'cache' or 'new download',
             'result':path to the file on disk with the downloaded data table}
    '''

    params = {
        'columns':'*',
        'filters':[
            {"paramName": idcol_to_use,
             "values":[str(objectid)]}
        ]
    }
    service = 'Mast.Catalogs.Filtered.Tic'

    return mast_query(service,
                      params,
                      jitter=jitter,
                      apiversion=apiversion,
                      forcefetch=forcefetch,
                      cachedir=cachedir,
                      verbose=verbose,
                      timeout=timeout,
                      refresh=refresh,
                      maxtimeout=maxtimeout,
                      maxtries=maxtries,
                      raiseonfail=raiseonfail)