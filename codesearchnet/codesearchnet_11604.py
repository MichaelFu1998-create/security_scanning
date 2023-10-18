def getAuthData(registry=None):
    ''' Poll the registry to get the result of a completed authentication
        (which, depending on the authentication the user chose or was directed
        to, will include a github or other access token)
    '''
    registry = registry or Registry_Base_URL
    url = '%s/tokens' % (
        registry
    )

    request_headers = _headersForRegistry(registry)

    logger.debug('poll for tokens... %s', request_headers)

    try:
        response = requests.get(url, headers=request_headers)
    except requests.RequestException as e:
        logger.debug(str(e))
        return None

    if response.status_code == requests.codes.unauthorized: #pylint: disable=no-member
        logger.debug('Unauthorised')
        return None
    elif response.status_code == requests.codes.not_found: #pylint: disable=no-member
        logger.debug('Not Found')
        return None

    body = response.text
    logger.debug('auth data response: %s' % body);
    r = {}

    parsed_response = ordered_json.loads(body)

    if 'error' in parsed_response:
        raise AuthError(parsed_response['error'])

    for token in parsed_response:
        if 'provider' in token and token['provider'] and 'accessToken' in token:
            r[token['provider']] = token['accessToken']
            break

    logger.debug('parsed auth tokens %s' % r);
    return r