def list_recent_datasets(lcc_server, nrecent=25):
    '''This lists recent publicly visible datasets available on the LCC-Server.

    If you have an LCC-Server API key present in `~/.astrobase/lccs/` that is
    associated with an LCC-Server user account, datasets that belong to this
    user will be returned as well, even if they are not visible to the public.

    Parameters
    ----------

    lcc_server : str
        This is the base URL of the LCC-Server to talk to.

    nrecent : int
        This indicates how many recent public datasets you want to list. This is
        always capped at 1000.

    Returns
    -------

    list of dicts
        Returns a list of dicts, with each dict containing info on each dataset.

    '''

    urlparams = {'nsets':nrecent}
    urlqs = urlencode(urlparams)

    url = '%s/api/datasets?%s' % (lcc_server, urlqs)

    try:

        LOGINFO(
            'getting list of recent publicly '
            'visible and owned datasets from %s' % (
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
        recent_datasets = json.loads(resp.read())['result']
        return recent_datasets

    except HTTPError as e:

        LOGERROR('could not retrieve recent datasets list, '
                 'URL used: %s, error code: %s, reason: %s' %
                 (url, e.code, e.reason))

        return None