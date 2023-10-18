def ensure_app_cache_dir(appname, *args):
    """
    Calls `get_app_cache_dir` but ensures the directory exists.

    Args:
        appname (str): the name of the application
        *args: any other subdirectories may be specified

    SeeAlso:
        get_app_cache_dir

    Example:
        >>> import ubelt as ub
        >>> dpath = ub.ensure_app_cache_dir('ubelt')
        >>> assert exists(dpath)
    """
    from ubelt import util_path
    dpath = get_app_cache_dir(appname, *args)
    util_path.ensuredir(dpath)
    return dpath