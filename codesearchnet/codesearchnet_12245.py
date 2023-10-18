def import_apikey(lcc_server, apikey_text_json):
    '''This imports an API key from text and writes it to the cache dir.

    Use this with the JSON text copied from the API key text box on your
    LCC-Server user home page. The API key will thus be tied to the privileges
    of that user account and can then access objects, datasets, and collections
    marked as private for the user only or shared with that user.

    Parameters
    ----------

    lcc_server : str
        The base URL of the LCC-Server to get the API key for.

    apikey_text_json : str
        The JSON string from the API key text box on the user's LCC-Server home
        page at `lcc_server/users/home`.

    Returns
    -------

    (apikey, expiry) : tuple
        This returns a tuple with the API key and its expiry date.

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

    respdict = json.loads(apikey_text_json)

    #
    # now that we have an API key dict, get the API key out of it and write it
    # to the APIKEYFILE
    #
    apikey = respdict['apikey']
    expires = respdict['expires']

    # write this to the apikey file

    if not os.path.exists(os.path.dirname(APIKEYFILE)):
        os.makedirs(os.path.dirname(APIKEYFILE))

    with open(APIKEYFILE,'w') as outfd:
        outfd.write('%s %s\n' % (apikey, expires))

    # chmod it to the correct value
    os.chmod(APIKEYFILE, 0o100600)

    LOGINFO('key fetched successfully from: %s. expires on: %s' % (lcc_server,
                                                                   expires))
    LOGINFO('written to: %s' % APIKEYFILE)

    return apikey, expires