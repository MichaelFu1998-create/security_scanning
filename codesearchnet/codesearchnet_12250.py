def get_dataset(lcc_server,
                dataset_id,
                strformat=False,
                page=1):
    '''This downloads a JSON form of a dataset from the specified lcc_server.

    If the dataset contains more than 1000 rows, it will be paginated, so you
    must use the `page` kwarg to get the page you want. The dataset JSON will
    contain the keys 'npages', 'currpage', and 'rows_per_page' to help with
    this. The 'rows' key contains the actual data rows as a list of tuples.

    The JSON contains metadata about the query that produced the dataset,
    information about the data table's columns, and links to download the
    dataset's products including the light curve ZIP and the dataset CSV.

    Parameters
    ----------

    lcc_server : str
        This is the base URL of the LCC-Server to talk to.

    dataset_id : str
        This is the unique setid of the dataset you want to get. In the results
        from the `*_search` functions above, this is the value of the
        `infodict['result']['setid']` key in the first item (the infodict) in
        the returned tuple.

    strformat : bool
        This sets if you want the returned data rows to be formatted in their
        string representations already. This can be useful if you're piping the
        returned JSON straight into some sort of UI and you don't want to deal
        with formatting floats, etc. To do this manually when strformat is set
        to False, look at the `coldesc` item in the returned dict, which gives
        the Python and Numpy string format specifiers for each column in the
        data table.

    page : int
        This sets which page of the dataset should be retrieved.

    Returns
    -------

    dict
        This returns the dataset JSON loaded into a dict.

    '''

    urlparams = {'strformat':1 if strformat else 0,
                 'page':page,
                 'json':1}
    urlqs = urlencode(urlparams)

    dataset_url = '%s/set/%s?%s' % (lcc_server, dataset_id, urlqs)

    LOGINFO('retrieving dataset %s from %s, using URL: %s ...' % (lcc_server,
                                                                  dataset_id,
                                                                  dataset_url))

    try:

        # check if we have an API key already
        have_apikey, apikey, expires = check_existing_apikey(lcc_server)

        # if not, get a new one
        if not have_apikey:
            apikey, expires = get_new_apikey(lcc_server)

        # if apikey is not None, add it in as an Authorization: Bearer [apikey]
        # header
        if apikey:
            headers = {'Authorization':'Bearer: %s' % apikey}
        else:
            headers = {}

        # hit the server
        req = Request(dataset_url, data=None, headers=headers)
        resp = urlopen(req)
        dataset = json.loads(resp.read())
        return dataset

    except Exception as e:

        LOGEXCEPTION('could not retrieve the dataset JSON!')
        return None