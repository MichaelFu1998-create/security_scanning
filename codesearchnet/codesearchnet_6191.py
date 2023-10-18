def send_status_response(environ, start_response, e, add_headers=None, is_head=False):
    """Start a WSGI response for a DAVError or status code."""
    status = get_http_status_string(e)
    headers = []
    if add_headers:
        headers.extend(add_headers)
    #    if 'keep-alive' in environ.get('HTTP_CONNECTION', '').lower():
    #        headers += [
    #            ('Connection', 'keep-alive'),
    #        ]

    if e in (HTTP_NOT_MODIFIED, HTTP_NO_CONTENT):
        # See paste.lint: these code don't have content
        start_response(
            status, [("Content-Length", "0"), ("Date", get_rfc1123_time())] + headers
        )
        return [b""]

    if e in (HTTP_OK, HTTP_CREATED):
        e = DAVError(e)
    assert isinstance(e, DAVError)

    content_type, body = e.get_response_page()
    if is_head:
        body = compat.b_empty

    assert compat.is_bytes(body), body  # If not, Content-Length is wrong!
    start_response(
        status,
        [
            ("Content-Type", content_type),
            ("Date", get_rfc1123_time()),
            ("Content-Length", str(len(body))),
        ]
        + headers,
    )
    return [body]