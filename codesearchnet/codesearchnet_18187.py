def sse_content(response, handler, **sse_kwargs):
    """
    Callback to collect the Server-Sent Events content of a response. Callbacks
    passed will receive event data.

    :param response:
        The response from the SSE request.
    :param handler:
        The handler for the SSE protocol.
    """
    # An SSE response must be 200/OK and have content-type 'text/event-stream'
    raise_for_not_ok_status(response)
    raise_for_header(response, 'Content-Type', 'text/event-stream')

    finished, _ = _sse_content_with_protocol(response, handler, **sse_kwargs)
    return finished