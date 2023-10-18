def request(http, uri, method='GET', body=None, headers=None,
            redirections=httplib2.DEFAULT_MAX_REDIRECTS,
            connection_type=None):
    """Make an HTTP request with an HTTP object and arguments.

    Args:
        http: httplib2.Http, an http object to be used to make requests.
        uri: string, The URI to be requested.
        method: string, The HTTP method to use for the request. Defaults
                to 'GET'.
        body: string, The payload / body in HTTP request. By default
              there is no payload.
        headers: dict, Key-value pairs of request headers. By default
                 there are no headers.
        redirections: int, The number of allowed 203 redirects for
                      the request. Defaults to 5.
        connection_type: httplib.HTTPConnection, a subclass to be used for
                         establishing connection. If not set, the type
                         will be determined from the ``uri``.

    Returns:
        tuple, a pair of a httplib2.Response with the status code and other
        headers and the bytes of the content returned.
    """
    # NOTE: Allowing http or http.request is temporary (See Issue 601).
    http_callable = getattr(http, 'request', http)
    return http_callable(uri, method=method, body=body, headers=headers,
                         redirections=redirections,
                         connection_type=connection_type)