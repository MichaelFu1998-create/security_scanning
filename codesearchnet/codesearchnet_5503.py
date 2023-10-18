def get_cors_options(appInstance, *dicts):
    """
    Compute CORS options for an application by combining the DEFAULT_OPTIONS,
    the app's configuration-specified options and any dictionaries passed. The
    last specified option wins.
    """
    options = DEFAULT_OPTIONS.copy()
    options.update(get_app_kwarg_dict(appInstance))
    if dicts:
        for d in dicts:
            options.update(d)

    return serialize_options(options)