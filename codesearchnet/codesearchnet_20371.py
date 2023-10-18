def paginate(request, response, items):
    """Paginate an iterable during a request.

    Magically splicling an iterable in our supported ORMs allows LIMIT and
    OFFSET queries. We should probably delegate this to the ORM or something
    in the future.
    """
    # TODO: support dynamic rangewords and page lengths
    # TODO: support multi-part range requests

    # Get the header
    header = request.headers.get('Range')
    if not header:
        # No range header; move along.
        return items

    # do some validation
    prefix = RANGE_SPECIFIER + '='
    if not header.find(prefix) == 0:
        # This is not using a range specifier that we understand
        raise exceptions.RequestedRangeNotSatisfiable()
    else:
        # Chop the prefix off the header and parse it
        ranges = parse(header[len(prefix):])

    ranges = list(ranges)
    if len(ranges) > 1:
        raise exceptions.RequestedRangeNotSatisfiable(
            'Multiple ranges in a single request is not yet supported.')
    start, end = ranges[0]

    # Make sure the length is not higher than the total number allowed.
    max_length = request.resource.count(items)
    end = min(end, max_length)

    response.status = client.PARTIAL_CONTENT
    response.headers['Content-Range'] = '%d-%d/%d' % (start, end, max_length)
    response.headers['Accept-Ranges'] = RANGE_SPECIFIER

    # Splice and return the items.
    items = items[start:end + 1]
    return items