def not_one_of(these):
    """Returns the current token if it is not found in the collection provided.
    
    The negative of one_of. 
    """
    ch = peek()
    desc = "not_one_of" + repr(these)
    try:
        if (ch is EndOfFile) or (ch in these):
            fail([desc])
    except TypeError:
        if ch != these:
            fail([desc])
    next()
    return ch