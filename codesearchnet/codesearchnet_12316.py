def tic_conesearch(
        ra,
        decl,
        radius_arcmin=5.0,
        apiversion='v0',
        forcefetch=False,
        cachedir='~/.astrobase/mast-cache',
        verbose=True,
        timeout=10.0,
        refresh=5.0,
        maxtimeout=90.0,
        maxtries=3,
        jitter=5.0,
        raiseonfail=False
):
    '''This runs a TESS Input Catalog cone search on MAST.

    If you use this, please cite the TIC paper (Stassun et al 2018;
    http://adsabs.harvard.edu/abs/2018AJ....156..102S). Also see the "living"
    TESS input catalog docs:

    https://docs.google.com/document/d/1zdiKMs4Ld4cXZ2DW4lMX-fuxAF6hPHTjqjIwGqnfjqI

    Also see: https://mast.stsci.edu/api/v0/_t_i_cfields.html for the fields
    returned by the service and present in the result JSON file.

    Parameters
    ----------

    ra,decl : float
        The center coordinates of the cone-search in decimal degrees.

    radius_arcmin : float
        The cone-search radius in arcminutes.

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

    params = {'ra':ra,
              'dec':decl,
              'radius':radius_arcmin/60.0}
    service = 'Mast.Catalogs.Tic.Cone'

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