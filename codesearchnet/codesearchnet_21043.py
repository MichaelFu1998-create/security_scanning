def one_of(these):
    """Returns the current token if is found in the collection provided.
    
    Fails otherwise.
    """
    ch = peek()
    try:
        if (ch is EndOfFile) or (ch not in these):
            fail(list(these))
    except TypeError:
        if ch != these:
            fail([these])
    next()
    return ch