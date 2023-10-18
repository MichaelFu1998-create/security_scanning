def normalize_modpath(modpath, hide_init=True, hide_main=False):
    """
    Normalizes __init__ and __main__ paths.

    Notes:
        Adds __init__ if reasonable, but only removes __main__ by default

    Args:
        hide_init (bool): if True, always return package modules
           as __init__.py files otherwise always return the dpath.
        hide_init (bool): if True, always strip away main files otherwise
           ignore __main__.py.

    CommandLine:
        xdoctest -m xdoctest.static_analysis normalize_modpath

    Example:
        >>> import xdoctest.static_analysis as static
        >>> modpath = static.__file__
        >>> assert static.normalize_modpath(modpath) == modpath.replace('.pyc', '.py')
        >>> dpath = dirname(modpath)
        >>> res0 = static.normalize_modpath(dpath, hide_init=0, hide_main=0)
        >>> res1 = static.normalize_modpath(dpath, hide_init=0, hide_main=1)
        >>> res2 = static.normalize_modpath(dpath, hide_init=1, hide_main=0)
        >>> res3 = static.normalize_modpath(dpath, hide_init=1, hide_main=1)
        >>> assert res0.endswith('__init__.py')
        >>> assert res1.endswith('__init__.py')
        >>> assert not res2.endswith('.py')
        >>> assert not res3.endswith('.py')
    """
    if six.PY2:
        if modpath.endswith('.pyc'):
            modpath = modpath[:-1]
    if hide_init:
        if basename(modpath) == '__init__.py':
            modpath = dirname(modpath)
            hide_main = True
    else:
        # add in init, if reasonable
        modpath_with_init = join(modpath, '__init__.py')
        if exists(modpath_with_init):
            modpath = modpath_with_init
    if hide_main:
        # We can remove main, but dont add it
        if basename(modpath) == '__main__.py':
            # corner case where main might just be a module name not in a pkg
            parallel_init = join(dirname(modpath), '__init__.py')
            if exists(parallel_init):
                modpath = dirname(modpath)
    return modpath