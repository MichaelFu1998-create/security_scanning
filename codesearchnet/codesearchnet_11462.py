def get_local_config(project_path, use_cache=True):
    """
    Produces a TidyPy configuration using the ``pyproject.toml`` in the
    project's directory.

    :param project_path: the path to the project that is going to be analyzed
    :type project_path: str
    :param use_cache:
        whether or not to use cached versions of any remote/referenced TidyPy
        configurations. If not specified, defaults to ``True``.
    :type use_cache: bool
    :rtype: dict
    """

    pyproject_path = os.path.join(project_path, 'pyproject.toml')

    if os.path.exists(pyproject_path):
        with open(pyproject_path, 'r') as config_file:
            config = pytoml.load(config_file)

        config = config.get('tool', {}).get('tidypy', {})
        config = merge_dict(get_default_config(), config)
        config = process_extensions(config, project_path, use_cache=use_cache)
        return config

    return None