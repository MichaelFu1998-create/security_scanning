def backend_version(backend, childprocess=None):
    """Back-end version.

    :param backend: back-end (examples:scrot, wx,..)
    :param childprocess: see :py:func:`grab`
    :return: version as string
    """
    if childprocess is None:
        childprocess = childprocess_default_value()
    if not childprocess:
        return _backend_version(backend)
    else:
        return run_in_childprocess(_backend_version, None, backend)