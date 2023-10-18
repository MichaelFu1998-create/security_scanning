def get_project_config(project_path, use_cache=True):
    """
    Produces the Tidypy configuration to use for the specified project.

    If a ``pyproject.toml`` exists, the configuration will be based on that. If
    not, the TidyPy configuration in the user's home directory will be used. If
    one does not exist, the default configuration will be used.

    :param project_path: the path to the project that is going to be analyzed
    :type project_path: str
    :param use_cache:
        whether or not to use cached versions of any remote/referenced TidyPy
        configurations. If not specified, defaults to ``True``.
    :type use_cache: bool
    :rtype: dict
    """

    return get_local_config(project_path, use_cache=use_cache) \
        or get_user_config(project_path, use_cache=use_cache) \
        or get_default_config()