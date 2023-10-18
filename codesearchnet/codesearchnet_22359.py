def Integer(name, base=10, encoding=None):
    """
    Match an integer route parameter.

    :type  name: `bytes`
    :param name: Route parameter name.

    :type  base: `int`
    :param base: Base to interpret the value in.

    :type  encoding: `bytes`
    :param encoding: Default encoding to assume if the ``Content-Type``
        header is lacking one.

    :return: ``callable`` suitable for use with `route` or `subroute`.
    """
    def _match(request, value):
        return name, query.Integer(
            value,
            base=base,
            encoding=contentEncoding(request.requestHeaders, encoding))
    return _match