def _parseAccept(headers):
    """
    Parse and sort an ``Accept`` header.

    The header is sorted according to the ``q`` parameter for each header value.

    @rtype: `OrderedDict` mapping `bytes` to `dict`
    @return: Mapping of media types to header parameters.
    """
    def sort(value):
        return float(value[1].get('q', 1))
    return OrderedDict(sorted(_splitHeaders(headers), key=sort, reverse=True))