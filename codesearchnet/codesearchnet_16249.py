def _getCallingContext():
    """
    Utility function for the RedisLogRecord.

    Returns the module, function, and lineno of the function 
    that called the logger.  
 
    We look way up in the stack.  The stack at this point is:
    [0] logger.py _getCallingContext (hey, that's me!)
    [1] logger.py __init__
    [2] logger.py makeRecord
    [3] _log
    [4] <logging method>
    [5] caller of logging method
    """
    frames = inspect.stack()

    if len(frames) > 4:
        context = frames[5]
    else:
        context = frames[0]

    modname = context[1]
    lineno = context[2]

    if context[3]:
        funcname = context[3]
    else:
        funcname = ""
        
    # python docs say you don't want references to
    # frames lying around.  Bad things can happen.
    del context
    del frames

    return modname, funcname, lineno