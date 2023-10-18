def contentEncoding(requestHeaders, encoding=None):
    """
    Extract an encoding from a ``Content-Type`` header.

    @type  requestHeaders: `twisted.web.http_headers.Headers`
    @param requestHeaders: Request headers.

    @type  encoding: `bytes`
    @param encoding: Default encoding to assume if the ``Content-Type``
        header is lacking one. Defaults to ``UTF-8``.

    @rtype: `bytes`
    @return: Content encoding.
    """
    if encoding is None:
        encoding = b'utf-8'
    headers = _splitHeaders(
        requestHeaders.getRawHeaders(b'Content-Type', []))
    if headers:
        return headers[0][1].get(b'charset', encoding)
    return encoding