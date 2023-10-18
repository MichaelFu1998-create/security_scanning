def read_and_discard_input(environ):
    """Read 1 byte from wsgi.input, if this has not been done yet.

    Returning a response without reading from a request body might confuse the
    WebDAV client.
    This may happen, if an exception like '401 Not authorized', or
    '500 Internal error' was raised BEFORE anything was read from the request
    stream.

    See GC issue 13, issue 23
    See http://groups.google.com/group/paste-users/browse_frm/thread/fc0c9476047e9a47?hl=en

    Note that with persistent sessions (HTTP/1.1) we must make sure, that the
    'Connection: closed' header is set with the response, to prevent reusing
    the current stream.
    """
    if environ.get("wsgidav.some_input_read") or environ.get("wsgidav.all_input_read"):
        return
    cl = get_content_length(environ)
    assert cl >= 0
    if cl == 0:
        return

    READ_ALL = True

    environ["wsgidav.some_input_read"] = 1
    if READ_ALL:
        environ["wsgidav.all_input_read"] = 1

    wsgi_input = environ["wsgi.input"]

    # TODO: check if still required after GC issue 24 is fixed
    if hasattr(wsgi_input, "_consumed") and hasattr(wsgi_input, "length"):
        # Seems to be Paste's httpserver.LimitedLengthFile
        # see http://groups.google.com/group/paste-users/browse_thread/thread/fc0c9476047e9a47/aa4a3aa416016729?hl=en&lnk=gst&q=.input#aa4a3aa416016729  # noqa
        # Consume something if nothing was consumed *and* work
        # around a bug where paste.httpserver allows negative lengths
        if wsgi_input._consumed == 0 and wsgi_input.length > 0:
            # This seems to work even if there's 10K of input.
            if READ_ALL:
                n = wsgi_input.length
            else:
                n = 1
            body = wsgi_input.read(n)
            _logger.debug(
                "Reading {} bytes from potentially unread httpserver.LimitedLengthFile: '{}'...".format(
                    n, body[:50]
                )
            )

    elif hasattr(wsgi_input, "_sock") and hasattr(wsgi_input._sock, "settimeout"):
        # Seems to be a socket
        try:
            # Set socket to non-blocking
            sock = wsgi_input._sock
            timeout = sock.gettimeout()
            sock.settimeout(0)
            # Read one byte
            try:
                if READ_ALL:
                    n = cl
                else:
                    n = 1
                body = wsgi_input.read(n)
                _logger.debug(
                    "Reading {} bytes from potentially unread POST body: '{}'...".format(
                        n, body[:50]
                    )
                )
            except socket.error as se:
                # se(10035, 'The socket operation could not complete without blocking')
                _logger.error("-> read {} bytes failed: {}".format(n, se))
            # Restore socket settings
            sock.settimeout(timeout)
        except Exception:
            _logger.error("--> wsgi_input.read(): {}".format(sys.exc_info()))