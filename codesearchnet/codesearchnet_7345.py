def streaming_to_client():
    """Puts the client logger into streaming mode, which sends
    unbuffered input through to the socket one character at a time.
    We also disable propagation so the root logger does not
    receive many one-byte emissions. This context handler
    was originally created for streaming Compose up's
    terminal output through to the client and should only be
    used for similarly complex circumstances."""
    for handler in client_logger.handlers:
        if hasattr(handler, 'append_newlines'):
            break
    else:
        handler = None
    old_propagate = client_logger.propagate
    client_logger.propagate = False
    if handler is not None:
        old_append = handler.append_newlines
        handler.append_newlines = False
    yield
    client_logger.propagate = old_propagate
    if handler is not None:
        handler.append_newlines = old_append