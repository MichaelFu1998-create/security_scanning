def check_existing_apikey(lcc_server):
    '''This validates if an API key for the specified LCC-Server is available.

    API keys are stored using the following file scheme::

        ~/.astrobase/lccs/apikey-domain.of.lccserver.org

    e.g. for the HAT LCC-Server at https://data.hatsurveys.org::

        ~/.astrobase/lccs/apikey-https-data.hatsurveys.org

    Parameters
    ----------

    lcc_server : str
        The base URL of the LCC-Server for which the existence of API keys will
        be checked.

    Returns
    -------

    (apikey_ok, apikey_str, expiry) : tuple
        The returned tuple contains the status of the API key, the API key
        itself if present, and its expiry date if present.

    '''

    USERHOME = os.path.expanduser('~')
    APIKEYFILE = os.path.join(USERHOME,
                              '.astrobase',
                              'lccs',
                              'apikey-%s' % lcc_server.replace(
                                  'https://',
                                  'https-'
                              ).replace(
                                  'http://',
                                  'http-'
                              ))

    if os.path.exists(APIKEYFILE):

        # check if this file is readable/writeable by user only
        fileperm = oct(os.stat(APIKEYFILE)[stat.ST_MODE])

        if fileperm == '0100600' or fileperm == '0o100600':

            with open(APIKEYFILE) as infd:
                apikey, expires = infd.read().strip('\n').split()

            # get today's datetime
            now = datetime.now(utc)

            if sys.version_info[:2] < (3,7):
                # this hideous incantation is required for lesser Pythons
                expdt = datetime.strptime(
                    expires.replace('Z',''),
                    '%Y-%m-%dT%H:%M:%S.%f'
                ).replace(tzinfo=utc)
            else:
                expdt = datetime.fromisoformat(expires.replace('Z','+00:00'))

            if now > expdt:
                LOGERROR('API key has expired. expiry was on: %s' % expires)
                return False, apikey, expires
            else:
                return True, apikey, expires

        else:
            LOGWARNING('The API key file %s has bad permissions '
                       'and is insecure, not reading it.\n'
                       '(you need to chmod 600 this file)'
                       % APIKEYFILE)

            return False, None, None
    else:
        LOGWARNING('No LCC-Server API key '
                   'found in: {apikeyfile}'.format(apikeyfile=APIKEYFILE))

        return False, None, None