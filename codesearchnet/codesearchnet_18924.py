def __locate_driver_named(name):
    """Searchs __modules for a driver named @arg name.

    @returns the package for driver @arg name or None if one can't be found.
    """
    global __modules

    if type(__modules) is not list:
        __modules = list(__modules)

    ms = [d for d in __modules if d.ahioDriverInfo.NAME == name]
    if not ms:
        return None
    return ms[0]