def object_info(lcc_server, objectid, db_collection_id):
    '''This gets information on a single object from the LCC-Server.

    Returns a dict with all of the available information on an object, including
    finding charts, comments, object type and variability tags, and
    period-search results (if available).

    If you have an LCC-Server API key present in `~/.astrobase/lccs/` that is
    associated with an LCC-Server user account, objects that are visible to this
    user will be returned, even if they are not visible to the public. Use this
    to look up objects that have been marked as 'private' or 'shared'.

    NOTE: you can pass the result dict returned by this function directly into
    the `astrobase.checkplot.checkplot_pickle_to_png` function, e.g.::

        astrobase.checkplot.checkplot_pickle_to_png(result_dict,
                                                    'object-%s-info.png' %
                                                    result_dict['objectid'])

    to generate a quick PNG overview of the object information.

    Parameters
    ----------

    lcc_server : str
        This is the base URL of the LCC-Server to talk to.

    objectid : str
        This is the unique database ID of the object to retrieve info for. This
        is always returned as the `db_oid` column in LCC-Server search results.

    db_collection_id : str
        This is the collection ID which will be searched for the object. This is
        always returned as the `collection` column in LCC-Server search results.

    Returns
    -------

    dict
        A dict containing the object info is returned. Some important items in
        the result dict:

        - `objectinfo`: all object magnitude, color, GAIA cross-match, and
          object type information available for this object

        - `objectcomments`: comments on the object's variability if available

        - `varinfo`: variability comments, variability features, type tags,
          period and epoch information if available

        - `neighbors`: information on the neighboring objects of this object in
          its parent light curve collection

        - `xmatch`: information on any cross-matches to external catalogs
          (e.g. KIC, EPIC, TIC, APOGEE, etc.)

        - `finderchart`: a base-64 encoded PNG image of the object's DSS2 RED
          finder chart. To convert this to an actual PNG, try the function:
          `astrobase.checkplot.pkl_io._b64_to_file`.

        - `magseries`: a base-64 encoded PNG image of the object's light
          curve. To convert this to an actual PNG, try the function:
          `astrobase.checkplot.pkl_io._b64_to_file`.

        - `pfmethods`: a list of period-finding methods applied to the object if
          any. If this list is present, use the keys in it to get to the actual
          period-finding results for each method. These will contain base-64
          encoded PNGs of the periodogram and phased light curves using the best
          three peaks in the periodogram, as well as period and epoch
          information.

    '''

    urlparams = {
        'objectid':objectid,
        'collection':db_collection_id
    }

    urlqs = urlencode(urlparams)
    url = '%s/api/object?%s' % (lcc_server, urlqs)

    try:

        LOGINFO(
            'getting info for %s in collection %s from %s' % (
                objectid,
                db_collection_id,
                lcc_server
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
        objectinfo = json.loads(resp.read())['result']
        return objectinfo

    except HTTPError as e:

        if e.code == 404:

            LOGERROR(
                'additional info for object %s not '
                'found in collection: %s' % (objectid,
                                             db_collection_id)
            )

        else:

            LOGERROR('could not retrieve object info, '
                     'URL used: %s, error code: %s, reason: %s' %
                     (url, e.code, e.reason))


        return None