def _build_google_client(service, api_version, http_auth):
    """
    Google build client helper.

    :param service: service to build client for
    :type service: ``str``

    :param api_version: API version to use.
    :type api_version: ``str``

    :param http_auth: Initialized HTTP client to use.
    :type http_auth: ``object``

    :return: google-python-api client initialized to use 'service'
    :rtype: ``object``
    """
    client = build(service, api_version, http=http_auth)
    return client