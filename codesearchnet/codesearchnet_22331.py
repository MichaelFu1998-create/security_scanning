def parse(expected, query):
    """
    Parse query parameters.

    :type  expected: `dict` mapping `bytes` to `callable`
    :param expected: Mapping of query argument names to argument parsing
        callables.

    :type  query: `dict` mapping `bytes` to `list` of `bytes`
    :param query: Mapping of query argument names to lists of argument values,
        this is the form that Twisted Web's `IRequest.args
        <twisted:twisted.web.iweb.IRequest.args>` value takes.

    :rtype: `dict` mapping `bytes` to `object`
    :return: Mapping of query argument names to parsed argument values.
    """
    return dict(
        (key, parser(query.get(key, [])))
        for key, parser in expected.items())