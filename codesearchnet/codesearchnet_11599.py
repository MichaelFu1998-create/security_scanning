def listOwners(namespace, name, registry=None):
    ''' List the owners of a module or target (owners are the people with
        permission to publish versions and add/remove the owners).
    '''
    registry = registry or Registry_Base_URL

    url = '%s/%s/%s/owners' % (
        registry,
        namespace,
        name
    )

    request_headers = _headersForRegistry(registry)

    response = requests.get(url, headers=request_headers)

    if response.status_code == 404:
        logger.error('no such %s, "%s"' % (namespace[:-1], name))
        return None

    # raise exceptions for other errors - the auth decorators handle these and
    # re-try if appropriate
    response.raise_for_status()

    return ordered_json.loads(response.text)