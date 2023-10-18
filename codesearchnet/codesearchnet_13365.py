def _move_session_handler(handlers):
    """Find a SessionHandler instance in the list and move it to the beginning.
    """
    index = 0
    for i, handler in enumerate(handlers):
        if isinstance(handler, SessionHandler):
            index = i
            break
    if index:
        handlers[:index + 1] = [handlers[index]] + handlers[:index]