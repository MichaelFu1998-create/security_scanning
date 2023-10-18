def prepare_args(config, bootstrap):
    """Convert config dict to command line args line.

    :param config: Configuration dict.
    :param bootstrap: Bootstrapper configuration dict.
    """
    config = copy.deepcopy(config)
    environ = dict(copy.deepcopy(os.environ))

    data = {'env': bootstrap['env'],
            'pip': pip_cmd(bootstrap['env'], '', return_path=True),
            'requirements': bootstrap['requirements']}
    environ.update(data)

    if isinstance(config, string_types):
        return config.format(**environ)

    for key, value in iteritems(config):
        if not isinstance(value, string_types):
            continue
        config[key] = value.format(**environ)

    return config_to_args(config)