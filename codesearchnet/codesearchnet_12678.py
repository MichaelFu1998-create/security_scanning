def _tailCallback(f, uid):
    """
    This is the "callable" version of the continuation, which sould only
    be accessible from the inside of the function to be continued. An
    attribute called "C" can be used in order to get back the public
    version of the continuation (for passing the continuation to another
    function).
    """
    def t(*args):
        raise _TailCall(f, args, uid)
    t.C = f
    return t