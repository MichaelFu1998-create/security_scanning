def ref(function, callback=None):
    """
    Returns a weak reference to the given method or function.
    If the callback argument is not None, it is called as soon
    as the referenced function is garbage deleted.

    :type  function: callable
    :param function: The function to reference.
    :type  callback: callable
    :param callback: Called when the function dies.
    """
    try:
        function.__func__
    except AttributeError:
        return _WeakMethodFree(function, callback)
    return _WeakMethodBound(function, callback)