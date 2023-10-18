def submit_post_searchquery(url, data, apikey):
    '''This submits a POST query to an LCC-Server search API endpoint.

    Handles streaming of the results, and returns the final JSON stream. Also
    handles results that time out.

    Parameters
    ----------

    url : str
        The URL of the search API endpoint to hit. This is something like
        `https://data.hatsurveys.org/api/conesearch`

    data : dict
        A dict of the search query parameters to pass to the search service.

    apikey : str
        The API key to use to access the search service. API keys are required
        for all POST request made to an LCC-Server's API endpoints.

    Returns
    -------

    (status_flag, data_dict, dataset_id) : tuple
        This returns a tuple containing the status of the request: ('complete',
        'failed', 'background', etc.), a dict parsed from the JSON result of the
        request, and a dataset ID, which can be used to reconstruct the URL on
        the LCC-Server where the results can be browsed.

    '''

    # first, we need to convert any columns and collections items to broken out
    # params
    postdata = {}

    for key in data:

        if key == 'columns':
            postdata['columns[]'] = data[key]
        elif key == 'collections':
            postdata['collections[]'] = data[key]
        else:
            postdata[key] = data[key]

    # do the urlencode with doseq=True
    # we also need to encode to bytes
    encoded_postdata = urlencode(postdata, doseq=True).encode()

    # if apikey is not None, add it in as an Authorization: Bearer [apikey]
    # header
    if apikey:
        headers = {'Authorization':'Bearer: %s' % apikey}
    else:
        headers = {}

    LOGINFO('submitting search query to LCC-Server API URL: %s' % url)

    try:

        # hit the server with a POST request
        req = Request(url, data=encoded_postdata, headers=headers)
        resp = urlopen(req)

        if resp.code == 200:

            # we'll iterate over the lines in the response
            # this works super-well for ND-JSON!
            for line in resp:

                data = json.loads(line)
                msg = data['message']
                status = data['status']

                if status != 'failed':
                    LOGINFO('status: %s, %s' % (status, msg))
                else:
                    LOGERROR('status: %s, %s' % (status, msg))

                # here, we'll decide what to do about the query

                # completed query or query sent to background...
                if status in ('ok','background'):

                    setid = data['result']['setid']
                    # save the data pickle to astrobase lccs directory
                    outpickle = os.path.join(os.path.expanduser('~'),
                                             '.astrobase',
                                             'lccs',
                                             'query-%s.pkl' % setid)
                    if not os.path.exists(os.path.dirname(outpickle)):
                        os.makedirs(os.path.dirname(outpickle))

                    with open(outpickle,'wb') as outfd:
                        pickle.dump(data, outfd, pickle.HIGHEST_PROTOCOL)
                        LOGINFO('saved query info to %s, use this to '
                                'download results later with '
                                'retrieve_dataset_files' % outpickle)

                    # we're done at this point, return
                    return status, data, data['result']['setid']

                # the query probably failed...
                elif status == 'failed':

                    # we're done at this point, return
                    return status, data, None


        # if the response was not OK, then we probably failed
        else:

            try:
                data = json.load(resp)
                msg = data['message']

                LOGERROR(msg)
                return 'failed', None, None

            except Exception as e:

                LOGEXCEPTION('failed to submit query to %s' % url)
                return 'failed', None, None

    except HTTPError as e:

        LOGERROR('could not submit query to LCC API at: %s' % url)
        LOGERROR('HTTP status code was %s, reason: %s' % (e.code, e.reason))
        return 'failed', None, None