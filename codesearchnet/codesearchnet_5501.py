def set_cors_headers(resp, options):
    """
    Performs the actual evaluation of Flas-CORS options and actually
    modifies the response object.

    This function is used both in the decorator and the after_request
    callback
    """

    # If CORS has already been evaluated via the decorator, skip
    if hasattr(resp, FLASK_CORS_EVALUATED):
        LOG.debug('CORS have been already evaluated, skipping')
        return resp

    # Some libraries, like OAuthlib, set resp.headers to non Multidict
    # objects (Werkzeug Headers work as well). This is a problem because
    # headers allow repeated values.
    if (not isinstance(resp.headers, Headers)
           and not isinstance(resp.headers, MultiDict)):
        resp.headers = MultiDict(resp.headers)

    headers_to_set = get_cors_headers(options, request.headers, request.method)

    LOG.debug('Settings CORS headers: %s', str(headers_to_set))

    for k, v in headers_to_set.items():
        resp.headers.add(k, v)

    return resp