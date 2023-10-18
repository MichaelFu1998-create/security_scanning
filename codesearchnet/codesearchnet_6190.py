def parse_xml_body(environ, allow_empty=False):
    """Read request body XML into an etree.Element.

    Return None, if no request body was sent.
    Raise HTTP_BAD_REQUEST, if something else went wrong.

    TODO: this is a very relaxed interpretation: should we raise HTTP_BAD_REQUEST
    instead, if CONTENT_LENGTH is missing, invalid, or 0?

    RFC: For compatibility with HTTP/1.0 applications, HTTP/1.1 requests containing
    a message-body MUST include a valid Content-Length header field unless the
    server is known to be HTTP/1.1 compliant.
    If a request contains a message-body and a Content-Length is not given, the
    server SHOULD respond with 400 (bad request) if it cannot determine the
    length of the message, or with 411 (length required) if it wishes to insist
    on receiving a valid Content-Length."

    So I'd say, we should accept a missing CONTENT_LENGTH, and try to read the
    content anyway.
    But WSGI doesn't guarantee to support input.read() without length(?).
    At least it locked, when I tried it with a request that had a missing
    content-type and no body.

    Current approach: if CONTENT_LENGTH is

    - valid and >0:
      read body (exactly <CONTENT_LENGTH> bytes) and parse the result.
    - 0:
      Assume empty body and return None or raise exception.
    - invalid (negative or not a number:
      raise HTTP_BAD_REQUEST
    - missing:
      NOT: Try to read body until end and parse the result.
      BUT: assume '0'
    - empty string:
      WSGI allows it to be empty or absent: treated like 'missing'.
    """
    #
    clHeader = environ.get("CONTENT_LENGTH", "").strip()
    #    content_length = -1 # read all of stream
    if clHeader == "":
        # No Content-Length given: read to end of stream
        # TODO: etree.parse() locks, if input is invalid?
        #        pfroot = etree.parse(environ["wsgi.input"]).getroot()
        # requestbody = environ["wsgi.input"].read()  # TODO: read() should be
        # called in a loop?
        requestbody = ""
    else:
        try:
            content_length = int(clHeader)
            if content_length < 0:
                raise DAVError(HTTP_BAD_REQUEST, "Negative content-length.")
        except ValueError:
            raise DAVError(HTTP_BAD_REQUEST, "content-length is not numeric.")

        if content_length == 0:
            requestbody = ""
        else:
            requestbody = environ["wsgi.input"].read(content_length)
            environ["wsgidav.all_input_read"] = 1

    if requestbody == "":
        if allow_empty:
            return None
        else:
            raise DAVError(HTTP_BAD_REQUEST, "Body must not be empty.")

    try:
        rootEL = etree.fromstring(requestbody)
    except Exception as e:
        raise DAVError(HTTP_BAD_REQUEST, "Invalid XML format.", src_exception=e)

    # If dumps of the body are desired, then this is the place to do it pretty:
    if environ.get("wsgidav.dump_request_body"):
        _logger.info(
            "{} XML request body:\n{}".format(
                environ["REQUEST_METHOD"],
                compat.to_native(xml_to_bytes(rootEL, pretty_print=True)),
            )
        )
        environ["wsgidav.dump_request_body"] = False

    return rootEL