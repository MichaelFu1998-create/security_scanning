def mast_query(service,
               params,
               data=None,
               apiversion='v0',
               forcefetch=False,
               cachedir='~/.astrobase/mast-cache',
               verbose=True,
               timeout=10.0,
               refresh=5.0,
               maxtimeout=90.0,
               maxtries=3,
               raiseonfail=False,
               jitter=5.0):
    '''This queries the STScI MAST service for catalog data.

    All results are downloaded as JSON files that are written to `cachedir`.

    Parameters
    ----------

    service : str
        This is the name of the service to use. See
        https://mast.stsci.edu/api/v0/_services.html for a list of all available
        services.

    params : dict
        This is a dict containing the input params to the service as described
        on its details page linked in the `service description page on MAST
        <https://mast.stsci.edu/api/v0/_services.html>`_.

    data : dict or None
        This contains optional data to upload to the service.

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

    raiseonfail : bool
        If this is True, the function will raise an Exception if something goes
        wrong, instead of returning None.

    jitter : float
        This is used to control the scale of the random wait in seconds before
        starting the query. Useful in parallelized situations.

    Returns
    -------

    dict
        This returns a dict of the following form::

            {'params':dict of the input params used for the query,
             'provenance':'cache' or 'new download',
             'result':path to the file on disk with the downloaded data table}

    '''

    # this matches:
    # https://mast.stsci.edu/api/v0/class_mashup_1_1_mashup_request.html
    inputparams = {
        'format':'json',
        'params':params,
        'service':service,
        'timeout':timeout,
    }

    if data is not None:
        inputparams['data'] = data

    # see if the cachedir exists
    if '~' in cachedir:
        cachedir = os.path.expanduser(cachedir)
    if not os.path.exists(cachedir):
        os.makedirs(cachedir)

    # generate the cachefname and look for it
    xcachekey = '-'.join([repr(inputparams[x])
                          for x in sorted(inputparams.keys())])
    cachekey = hashlib.sha256(xcachekey.encode()).hexdigest()

    cachefname = os.path.join(
        cachedir,
        '%s.json' % (cachekey,)
    )
    provenance = 'cache'

    #####################
    ## RUN A NEW QUERY ##
    #####################

    # otherwise, we check the cache if it's done already, or run it again if not
    if forcefetch or (not os.path.exists(cachefname)):

        time.sleep(random.randint(1,jitter))

        provenance = 'new download'
        waitdone = False
        timeelapsed = 0.0
        ntries = 1

        url = MAST_URLS[apiversion]['url']
        formdata = {'request':json.dumps(inputparams)}

        while (not waitdone) or (ntries < maxtries):

            if timeelapsed > maxtimeout:
                retdict = None
                break

            try:

                resp = requests.post(url,
                                     data=formdata,
                                     # we'll let the service time us out first
                                     # if that fails, we'll timeout ourselves
                                     timeout=timeout+1.0)
                resp.raise_for_status()

                respjson = resp.json()

                if respjson['status'] == 'COMPLETE':

                    data = respjson['data']
                    nrows = len(data)

                    if nrows > 0:

                        with open(cachefname, 'w') as outfd:
                            json.dump(respjson, outfd)

                        retdict = {
                            'params':inputparams,
                            'provenance':provenance,
                            'cachefname':cachefname
                        }
                        waitdone = True

                        if verbose:
                            LOGINFO('query successful. nmatches: %s' % nrows)

                        break

                    else:

                        LOGERROR(
                            'no matching objects found for inputparams: %r' %
                            inputparams
                        )
                        retdict = None
                        waitdone = True
                        break

                # if we're still executing after the initial timeout is done
                elif respjson['status'] == 'EXECUTING':

                    if verbose:
                        LOGINFO('query is still executing, '
                                'waiting %s seconds to retry...' % refresh)
                    waitdone = False
                    time.sleep(refresh)
                    timeelapsed = timeelapsed + refresh
                    retdict = None

                else:

                    LOGERROR('Query failed! Message from service: %s' %
                             respjson['msg'])
                    retdict = None
                    waitdone = True
                    break

            except requests.exceptions.Timeout as e:

                if verbose:
                    LOGWARNING('MAST query try timed out, '
                               'site is probably down. '
                               'Waiting for %s seconds to try again...' %
                               refresh)
                waitdone = False
                time.sleep(refresh)
                timeelapsed = timeelapsed + refresh
                retdict = None

            except KeyboardInterrupt as e:

                LOGERROR('MAST request wait aborted for '
                         '%s' % repr(inputparams))
                return None

            except Exception as e:

                LOGEXCEPTION('MAST query failed!')

                if raiseonfail:
                    raise

                return None

            #
            # increment number of tries at the bottom of the loop
            #
            ntries = ntries + 1

        #
        # done with waiting for completion
        #
        if retdict is None:

            LOGERROR('Timed out, errored out, or reached maximum number '
                     'of tries with no response. Query was: %r' % inputparams)
            return None

        else:

            return retdict

    # otherwise, get the file from the cache
    else:

        if verbose:
            LOGINFO('getting cached MAST query result for '
                    'request: %s' %
                    (repr(inputparams)))

        retdict = {
            'params':inputparams,
            'provenance':provenance,
            'cachefname':cachefname
        }

        return retdict