def list_lc_collections(lcc_server):
    '''This lists all light curve collections made available on the LCC-Server.

    If you have an LCC-Server API key present in `~/.astrobase/lccs/` that is
    associated with an LCC-Server user account, light curve collections visible
    to this user will be returned as well, even if they are not visible to the
    public.

    Parameters
    ----------

    lcc_server : str
        The base URL of the LCC-Server to talk to.

    Returns
    -------

    dict
        Returns a dict containing lists of info items per collection. This
        includes collection_ids, lists of columns, lists of indexed columns,
        lists of full-text indexed columns, detailed column descriptions, number
        of objects in each collection, collection sky coverage, etc.

    '''

    url = '%s/api/collections' % lcc_server

    try:

        LOGINFO(
            'getting list of recent publicly visible '
            'and owned LC collections from %s' % (
                lcc_server,
            )
        )

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
        req = Request(url, data=None, headers=headers)
        resp = urlopen(req)
        lcc_list = json.loads(resp.read())['result']['collections']
        return lcc_list

    except HTTPError as e:

        LOGERROR('could not retrieve list of collections, '
                 'URL used: %s, error code: %s, reason: %s' %
                 (url, e.code, e.reason))

        return None