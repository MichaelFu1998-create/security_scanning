def _detect_gce_environment():
    """Determine if the current environment is Compute Engine.

    Returns:
        Boolean indicating whether or not the current environment is Google
        Compute Engine.
    """
    # NOTE: The explicit ``timeout`` is a workaround. The underlying
    #       issue is that resolving an unknown host on some networks will take
    #       20-30 seconds; making this timeout short fixes the issue, but
    #       could lead to false negatives in the event that we are on GCE, but
    #       the metadata resolution was particularly slow. The latter case is
    #       "unlikely".
    http = transport.get_http_object(timeout=GCE_METADATA_TIMEOUT)
    try:
        response, _ = transport.request(
            http, _GCE_METADATA_URI, headers=_GCE_HEADERS)
        return (
            response.status == http_client.OK and
            response.get(_METADATA_FLAVOR_HEADER) == _DESIRED_METADATA_FLAVOR)
    except socket.error:  # socket.timeout or socket.error(64, 'Host is down')
        logger.info('Timeout attempting to reach GCE metadata service.')
        return False