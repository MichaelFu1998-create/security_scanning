def _c_func(func, restype, argtypes, errcheck=None):
    """Wrap c function setting prototype."""
    func.restype = restype
    func.argtypes = argtypes
    if errcheck is not None:
        func.errcheck = errcheck
    return func