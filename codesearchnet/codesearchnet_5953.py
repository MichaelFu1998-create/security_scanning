def _googleauth(key_file=None, scopes=[], user_agent=None):
    """
    Google http_auth helper.

    If key_file is not specified, default credentials will be used.

    If scopes is specified (and key_file), will be used instead of DEFAULT_SCOPES

    :param key_file: path to key file to use. Default is None
    :type key_file: ``str``

    :param scopes: scopes to set.  Default is DEFAUL_SCOPES
    :type scopes: ``list``

    :param user_agent: User Agent string to use in requests. Default is None.
    :type http_auth: ``str`` or None

    :return: HTTPLib2 authorized client.
    :rtype: :class: `HTTPLib2`
    """
    if key_file:
        if not scopes:
            scopes = DEFAULT_SCOPES
        creds = ServiceAccountCredentials.from_json_keyfile_name(key_file,
                                                                 scopes=scopes)
    else:
        creds = GoogleCredentials.get_application_default()
    http = Http()
    if user_agent:
        http = set_user_agent(http, user_agent)
    http_auth = creds.authorize(http)
    return http_auth