def get_gdal_options(opts, is_remote=False):
    """
    Return a merged set of custom and default GDAL/rasterio Env options.

    If is_remote is set to True, the default GDAL_HTTP_OPTS are appended.

    Parameters
    ----------
    opts : dict or None
        Explicit GDAL options.
    is_remote : bool
        Indicate whether Env is for a remote file.

    Returns
    -------
    dictionary
    """
    user_opts = {} if opts is None else dict(**opts)
    if is_remote:
        return dict(GDAL_HTTP_OPTS, **user_opts)
    else:
        return user_opts