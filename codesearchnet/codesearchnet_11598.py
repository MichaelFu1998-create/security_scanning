def unpublish(namespace, name, version, registry=None):
    ''' Try to unpublish a recently published version. Return any errors that
        occur.
    '''
    registry = registry or Registry_Base_URL

    url = '%s/%s/%s/versions/%s' % (
        registry,
        namespace,
        name,
        version
    )

    headers = _headersForRegistry(registry)
    response = requests.delete(url, headers=headers)
    response.raise_for_status()

    return None