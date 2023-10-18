def fetch_url(url, method='GET', user_agent='django-oembed', timeout=SOCKET_TIMEOUT):
    """
    Fetch response headers and data from a URL, raising a generic exception
    for any kind of failure.
    """
    sock = httplib2.Http(timeout=timeout)
    request_headers = {
        'User-Agent': user_agent,
        'Accept-Encoding': 'gzip'}
    try:
        headers, raw = sock.request(url, headers=request_headers, method=method)
    except:
        raise OEmbedHTTPException('Error fetching %s' % url)
    return headers, raw