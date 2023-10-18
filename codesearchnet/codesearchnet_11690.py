def runs_once(meth):
    """
    A wrapper around Fabric's runs_once() to support our dryrun feature.
    """
    from burlap.common import get_dryrun, runs_once_methods
    if get_dryrun():
        pass
    else:
        runs_once_methods.append(meth)
        _runs_once(meth)
    return meth