def _sse_content_with_protocol(response, handler, **sse_kwargs):
    """
    Sometimes we need the protocol object so that we can manipulate the
    underlying transport in tests.
    """
    protocol = SseProtocol(handler, **sse_kwargs)
    finished = protocol.when_finished()

    response.deliverBody(protocol)

    return finished, protocol