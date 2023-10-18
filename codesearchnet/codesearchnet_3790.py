def config_from_environment():
    """Read tower-cli config values from the environment if present, being
    careful not to override config values that were explicitly passed in.
    """
    kwargs = {}
    for k in CONFIG_OPTIONS:
        env = 'TOWER_' + k.upper()
        v = os.getenv(env, None)
        if v is not None:
            kwargs[k] = v
    return kwargs