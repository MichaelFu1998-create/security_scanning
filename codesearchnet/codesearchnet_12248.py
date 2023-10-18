def cone_search(lcc_server,
                center_ra,
                center_decl,
                radiusarcmin=5.0,
                result_visibility='unlisted',
                email_when_done=False,
                collections=None,
                columns=None,
                filters=None,
                sortspec=None,
                samplespec=None,
                limitspec=None,
                download_data=True,
                outdir=None,
                maxtimeout=300.0,
                refresh=15.0):

    '''This runs a cone-search query.

    Parameters
    ----------

    lcc_server : str
        This is the base URL of the LCC-Server to talk to.  (e.g. for HAT, use:
        https://data.hatsurveys.org)

    center_ra,center_decl : float
        These are the central coordinates of the search to conduct. These can be
        either decimal degrees of type float, or sexagesimal coordinates of type
        str:

        - OK: 290.0, 45.0
        - OK: 15:00:00 +45:00:00
        - OK: 15 00 00.0 -45 00 00.0
        - NOT OK: 290.0 +45:00:00
        - NOT OK: 15:00:00 45.0

    radiusarcmin : float
        This is the search radius to use for the cone-search. This is in
        arcminutes. The maximum radius you can use is 60 arcminutes = 1 degree.

    result_visibility : {'private', 'unlisted', 'public'}
        This sets the visibility of the dataset produced from the search
        result::

               'private' -> the dataset and its products are not visible or
                            accessible by any user other than the one that
                            created the dataset.

               'unlisted' -> the dataset and its products are not visible in the
                             list of public datasets, but can be accessed if the
                             dataset URL is known

               'public' -> the dataset and its products are visible in the list
                           of public datasets and can be accessed by anyone.

    email_when_done : bool
        If True, the LCC-Server will email you when the search is complete. This
        will also set `download_data` to False. Using this requires an
        LCC-Server account and an API key tied to that account.

    collections : list of str or None
        This is a list of LC collections to search in. If this is None, all
        collections will be searched.

    columns : list of str or None
        This is a list of columns to return in the results. Matching objects'
        object IDs, RAs, DECs, and links to light curve files will always be
        returned so there is no need to specify these columns. If None, only
        these columns will be returned: 'objectid', 'ra', 'decl', 'lcfname'

    filters : str or None
        This is an SQL-like string to use to filter on database columns in the
        LCC-Server's collections. To see the columns available for a search,
        visit the Collections tab in the LCC-Server's browser UI. The filter
        operators allowed are::

            lt      -> less than
            gt      -> greater than
            ge      -> greater than or equal to
            le      -> less than or equal to
            eq      -> equal to
            ne      -> not equal to
            ct      -> contains text
            isnull  -> column value is null
            notnull -> column value is not null

        You may use the `and` and `or` operators between filter specifications
        to chain them together logically.

        Example filter strings::

            "(propermotion gt 200.0) and (sdssr lt 11.0)"
            "(dered_jmag_kmag gt 2.0) and (aep_000_stetsonj gt 10.0)"
            "(gaia_status ct 'ok') and (propermotion gt 300.0)"
            "(simbad_best_objtype ct 'RR') and (dered_sdssu_sdssg lt 0.5)"

    sortspec : tuple of two strs or None
        If not None, this should be a tuple of two items::

            ('column to sort by', 'asc|desc')

        This sets the column to sort the results by. For cone_search, the
        default column and sort order are 'dist_arcsec' and 'asc', meaning the
        distance from the search center in ascending order.

    samplespec : int or None
        If this is an int, will indicate how many rows from the initial search
        result will be uniformly random sampled and returned.

    limitspec : int or None
        If this is an int, will indicate how many rows from the initial search
        result to return in total.

        `sortspec`, `samplespec`, and `limitspec` are applied in this order:

            sample -> sort -> limit

    download_data : bool
        This sets if the accompanying data from the search results will be
        downloaded automatically. This includes the data table CSV, the dataset
        pickle file, and a light curve ZIP file. Note that if the search service
        indicates that your query is still in progress, this function will block
        until the light curve ZIP file becomes available. The maximum wait time
        in seconds is set by maxtimeout and the refresh interval is set by
        refresh.

        To avoid the wait block, set download_data to False and the function
        will write a pickle file to `~/.astrobase/lccs/query-[setid].pkl`
        containing all the information necessary to retrieve these data files
        later when the query is done. To do so, call the
        `retrieve_dataset_files` with the path to this pickle file (it will be
        returned).

    outdir : str or None
        If this is provided, sets the output directory of the downloaded dataset
        files. If None, they will be downloaded to the current directory.

    maxtimeout : float
        The maximum time in seconds to wait for the LCC-Server to respond with a
        result before timing out. You can use the `retrieve_dataset_files`
        function to get results later as needed.

    refresh : float
        The time to wait in seconds before pinging the LCC-Server to see if a
        search query has completed and dataset result files can be downloaded.

    Returns
    -------

    tuple
        Returns a tuple with the following elements::

            (search result status dict,
             search result CSV file path,
             search result LC ZIP path)

    '''

    # turn the input into a param dict

    coords = '%.5f %.5f %.1f' % (center_ra, center_decl, radiusarcmin)
    params = {
        'coords':coords
    }

    if collections:
        params['collections'] = collections
    if columns:
        params['columns'] = columns
    if filters:
        params['filters'] = filters
    if sortspec:
        params['sortspec'] = json.dumps([sortspec])
    if samplespec:
        params['samplespec'] = int(samplespec)
    if limitspec:
        params['limitspec'] = int(limitspec)

    params['visibility'] = result_visibility
    params['emailwhendone'] = email_when_done

    # we won't wait for the LC ZIP to complete if email_when_done = True
    if email_when_done:
        download_data = False

    # check if we have an API key already
    have_apikey, apikey, expires = check_existing_apikey(lcc_server)

    # if not, get a new one
    if not have_apikey:
        apikey, expires = get_new_apikey(lcc_server)

    # hit the server
    api_url = '%s/api/conesearch' % lcc_server

    searchresult = submit_post_searchquery(api_url, params, apikey)

    # check the status of the search
    status = searchresult[0]

    # now we'll check if we want to download the data
    if download_data:

        if status == 'ok':

            LOGINFO('query complete, downloading associated data...')
            csv, lczip, pkl = retrieve_dataset_files(searchresult,
                                                     outdir=outdir,
                                                     apikey=apikey)

            if pkl:
                return searchresult[1], csv, lczip, pkl
            else:
                return searchresult[1], csv, lczip

        elif status == 'background':

            LOGINFO('query is not yet complete, '
                    'waiting up to %.1f minutes, '
                    'updates every %s seconds (hit Ctrl+C to cancel)...' %
                    (maxtimeout/60.0, refresh))

            timewaited = 0.0

            while timewaited < maxtimeout:

                try:

                    time.sleep(refresh)
                    csv, lczip, pkl = retrieve_dataset_files(searchresult,
                                                             outdir=outdir,
                                                             apikey=apikey)

                    if (csv and os.path.exists(csv) and
                        lczip and os.path.exists(lczip)):

                        LOGINFO('all dataset products collected')
                        return searchresult[1], csv, lczip

                    timewaited = timewaited + refresh

                except KeyboardInterrupt:

                    LOGWARNING('abandoned wait for downloading data')
                    return searchresult[1], None, None

            LOGERROR('wait timed out.')
            return searchresult[1], None, None

        else:

            LOGERROR('could not download the data for this query result')
            return searchresult[1], None, None

    else:

        return searchresult[1], None, None