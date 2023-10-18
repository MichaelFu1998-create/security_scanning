def _matchRoute(components, request, segments, partialMatching):
    """
    Match a request path against our path components.

    The path components are always matched relative to their parent is in the
    resource hierarchy, in other words it is only possible to match URIs nested
    more deeply than the parent resource.

    :type  components: ``iterable`` of `bytes` or `callable`
    :param components: Iterable of path components, to match against the
        request, either static strings or dynamic parameters. As a convenience,
        a single `bytes` component containing ``/`` may be given instead of
        manually separating the components. If no components are given the null
        route is matched, this is the case where ``segments`` is empty.

    :type  segments: ``sequence`` of `bytes`
    :param segments: Sequence of path segments, from the request, to match
        against.

    :type  partialMatching: `bool`
    :param partialMatching: Allow partial matching against the request path?

    :rtype: 2-`tuple` of `dict` keyed on `bytes` and `list` of `bytes`
    :return: Pair of parameter results, mapping parameter names to processed
        values, and a list of the remaining request path segments. If there is
        no route match the result will be ``None`` and the original request path
        segments.
    """
    if len(components) == 1 and isinstance(components[0], bytes):
        components = components[0]
        if components[:1] == '/':
            components = components[1:]
        components = components.split('/')

    results = OrderedDict()
    NO_MATCH = None, segments
    remaining = list(segments)

    # Handle the null route.
    if len(segments) == len(components) == 0:
        return results, remaining

    for us, them in izip_longest(components, segments):
        if us is None:
            if partialMatching:
                # We've matched all of our components, there might be more
                # segments for something else to process.
                break
            else:
                return NO_MATCH
        elif them is None:
            # We've run out of path segments to match, so this route can't be
            # the matching one.
            return NO_MATCH

        if callable(us):
            name, match = us(request, them)
            if match is None:
                return NO_MATCH
            results[name] = match
        elif us != them:
            return NO_MATCH
        remaining.pop(0)

    return results, remaining