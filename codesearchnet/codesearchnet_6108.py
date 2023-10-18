def _get_checked_path(path, config, must_exist=True, allow_none=True):
    """Convert path to absolute if not None."""
    if path in (None, ""):
        if allow_none:
            return None
        raise ValueError("Invalid path {!r}".format(path))
    # Evaluate path relative to the folder of the config file (if any)
    config_file = config.get("_config_file")
    if config_file and not os.path.isabs(path):
        path = os.path.normpath(os.path.join(os.path.dirname(config_file), path))
    else:
        path = os.path.abspath(path)
    if must_exist and not os.path.exists(path):
        raise ValueError("Invalid path {!r}".format(path))
    return path