def Text(name, encoding=None):
    """
    Match a route parameter.

    `Any` is a synonym for `Text`.

    :type  name: `bytes`
    :param name: Route parameter name.

    :type  encoding: `bytes`
    :param encoding: Default encoding to assume if the ``Content-Type``
        header is lacking one.

    :return: ``callable`` suitable for use with `route` or `subroute`.
    """
    def _match(request, value):
        return name, query.Text(
            value,
            encoding=contentEncoding(request.requestHeaders, encoding))
    return _match