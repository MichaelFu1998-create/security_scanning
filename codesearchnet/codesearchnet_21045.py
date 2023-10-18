def satisfies(guard):
    """Returns the current token if it satisfies the guard function provided.
    
    Fails otherwise.
    This is the a generalisation of one_of.
    """
    i = peek()
    if (i is EndOfFile) or (not guard(i)):
        fail(["<satisfies predicate " + _fun_to_str(guard) + ">"])
    next()
    return i