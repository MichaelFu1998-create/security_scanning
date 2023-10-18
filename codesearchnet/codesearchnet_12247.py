def retrieve_dataset_files(searchresult,
                           getpickle=False,
                           outdir=None,
                           apikey=None):
    '''This retrieves a search result dataset's CSV and any LC zip files.

    Takes the output from the `submit_post_searchquery` function above or a
    pickle file generated from that function's output if the query timed out.

    Parameters
    ----------

    searchresult : str or tuple
        If provided as a str, points to the pickle file created using the output
        from the `submit_post_searchquery` function. If provided as a tuple,
        this is the result tuple from the `submit_post_searchquery` function.

    getpickle : False
        If this is True, will also download the dataset's pickle. Note that
        LCC-Server is a Python 3.6+ package (while lccs.py still works with
        Python 2.7) and it saves its pickles in pickle.HIGHEST_PROTOCOL for
        efficiency, so these pickles may be unreadable in lower Pythons. As an
        alternative, the dataset CSV contains the full data table and all the
        information about the dataset in its header, which is JSON
        parseable. You can also use the function `get_dataset` below to get the
        dataset pickle information in JSON form.

    outdir : None or str
        If this is a str, points to the output directory where the results will
        be placed. If it's None, they will be placed in the current directory.

    apikey : str or None
        If this is a str, uses the given API key to authenticate the download
        request. This is useful when you have a private dataset you want to get
        products for.

    Returns
    -------

    (local_dataset_csv, local_dataset_lczip, local_dataset_pickle) : tuple
        This returns a tuple containing paths to the dataset CSV, LC zipfile,
        and the dataset pickle if getpickle was set to True (None otherwise).

    '''

    # this handles the direct result case from submit_*_query functions
    if isinstance(searchresult, tuple):

        info, setid = searchresult[1:]

    # handles the case where we give the function a existing query pickle
    elif isinstance(searchresult, str) and os.path.exists(searchresult):

        with open(searchresult,'rb') as infd:
            info = pickle.load(infd)
        setid = info['result']['setid']

    else:

        LOGERROR('could not understand input, '
                 'we need a searchresult from the '
                 'lccs.submit_post_searchquery function or '
                 'the path to an existing query pickle')
        return None, None, None

    # now that we have everything, let's download some files!

    dataset_pickle = 'dataset-%s.pkl.gz' % setid
    dataset_csv = 'dataset-%s.csv' % setid
    dataset_lczip = 'lightcurves-%s.zip' % setid

    if outdir is None:
        localdir = os.getcwd()
    else:
        localdir = outdir

    server_scheme, server_netloc = urlparse(info['result']['seturl'])[:2]
    dataset_pickle_link = '%s://%s/d/%s' % (server_scheme,
                                            server_netloc,
                                            dataset_pickle)
    dataset_csv_link = '%s://%s/d/%s' % (server_scheme,
                                         server_netloc,
                                         dataset_csv)
    dataset_lczip_link = '%s://%s/p/%s' % (server_scheme,
                                           server_netloc,
                                           dataset_lczip)

    if getpickle:

        # get the dataset pickle
        LOGINFO('getting %s...' % dataset_pickle_link)
        try:

            if os.path.exists(os.path.join(localdir, dataset_pickle)):

                LOGWARNING('dataset pickle already exists, '
                           'not downloading again..')
                local_dataset_pickle = os.path.join(localdir,
                                                    dataset_pickle)

            else:

                # if apikey is not None, add it in as an Authorization: Bearer
                # [apikey] header
                if apikey:
                    headers = {'Authorization':'Bearer: %s' % apikey}
                else:
                    headers = {}

                req = Request(
                    dataset_pickle_link,
                    data=None,
                    headers=headers
                )
                resp = urlopen(req)

                # save the file
                LOGINFO('saving %s' % dataset_pickle)
                localf = os.path.join(localdir, dataset_pickle)
                with open(localf, 'wb') as outfd:
                    with resp:
                        data = resp.read()
                        outfd.write(data)

                LOGINFO('OK -> %s' % localf)
                local_dataset_pickle = localf

        except HTTPError as e:
            LOGERROR('could not download %s, '
                     'HTTP status code was: %s, reason: %s' %
                     (dataset_pickle_link, e.code, e.reason))
            local_dataset_pickle = None

    else:
        local_dataset_pickle = None


    # get the dataset CSV
    LOGINFO('getting %s...' % dataset_csv_link)
    try:

        if os.path.exists(os.path.join(localdir, dataset_csv)):

            LOGWARNING('dataset CSV already exists, not downloading again...')
            local_dataset_csv = os.path.join(localdir, dataset_csv)

        else:

            # if apikey is not None, add it in as an Authorization: Bearer
            # [apikey] header
            if apikey:
                headers = {'Authorization':'Bearer: %s' % apikey}
            else:
                headers = {}

            req = Request(
                dataset_csv_link,
                data=None,
                headers=headers
            )
            resp = urlopen(req)

            # save the file
            LOGINFO('saving %s' % dataset_csv)
            localf = os.path.join(localdir, dataset_csv)
            with open(localf, 'wb') as outfd:
                with resp:
                    data = resp.read()
                    outfd.write(data)

            LOGINFO('OK -> %s' % localf)
            local_dataset_csv = localf

    except HTTPError as e:

        LOGERROR('could not download %s, HTTP status code was: %s, reason: %s' %
                 (dataset_csv_link, e.code, e.reason))
        local_dataset_csv = None


    # get the dataset LC zip
    LOGINFO('getting %s...' % dataset_lczip_link)
    try:

        if os.path.exists(os.path.join(localdir, dataset_lczip)):

            LOGWARNING('dataset LC ZIP already exists, '
                       'not downloading again...')
            local_dataset_lczip = os.path.join(localdir, dataset_lczip)

        else:

            # if apikey is not None, add it in as an Authorization: Bearer
            # [apikey] header
            if apikey:
                headers = {'Authorization':'Bearer: %s' % apikey}
            else:
                headers = {}

            req = Request(
                dataset_lczip_link,
                data=None,
                headers=headers
            )
            resp = urlopen(req)

            # save the file
            LOGINFO('saving %s' % dataset_lczip)
            localf = os.path.join(localdir, dataset_lczip)
            with open(localf, 'wb') as outfd:
                with resp:
                    data = resp.read()
                    outfd.write(data)

            LOGINFO('OK -> %s' % localf)
            local_dataset_lczip = localf

    except HTTPError as e:
        LOGERROR('could not download %s, HTTP status code was: %s, reason: %s' %
                 (dataset_lczip_link, e.code, e.reason))
        local_dataset_lczip = None


    return local_dataset_csv, local_dataset_lczip, local_dataset_pickle