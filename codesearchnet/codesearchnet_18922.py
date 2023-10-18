def available_drivers():
    """Returns a list of available drivers names.
    """
    global __modules
    global __available

    if type(__modules) is not list:
        __modules = list(__modules)

    if not __available:
        __available = [d.ahioDriverInfo.NAME
                       for d in __modules
                       if d.ahioDriverInfo.AVAILABLE]

    return __available