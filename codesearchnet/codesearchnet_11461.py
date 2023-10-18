def get_user_config(project_path, use_cache=True):
    """
    Produces a TidyPy configuration that incorporates the configuration files
    stored in the current user's home directory.

    :param project_path: the path to the project that is going to be analyzed
    :type project_path: str
    :param use_cache:
        whether or not to use cached versions of any remote/referenced TidyPy
        configurations. If not specified, defaults to ``True``.
    :type use_cache: bool
    :rtype: dict
    """

    if sys.platform == 'win32':
        user_config = os.path.expanduser(r'~\\tidypy')
    else:
        user_config = os.path.join(
            os.getenv('XDG_CONFIG_HOME') or os.path.expanduser('~/.config'),
            'tidypy'
        )

    if os.path.exists(user_config):
        with open(user_config, 'r') as config_file:
            config = pytoml.load(config_file).get('tidypy', {})

        config = merge_dict(get_default_config(), config)
        config = process_extensions(config, project_path, use_cache=use_cache)
        return config

    return None