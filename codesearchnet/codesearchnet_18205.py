def get_single_header(headers, key):
    """
    Get a single value for the given key out of the given set of headers.

    :param twisted.web.http_headers.Headers headers:
        The set of headers in which to look for the header value
    :param str key:
        The header key
    """
    raw_headers = headers.getRawHeaders(key)
    if raw_headers is None:
        return None

    # Take the final header as the authorative
    header, _ = cgi.parse_header(raw_headers[-1])
    return header