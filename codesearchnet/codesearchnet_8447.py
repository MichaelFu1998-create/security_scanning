def env_to_dict(prefix, names):
    """
    Construct dict from environment variables named: PREFIX_NAME

    @returns dict of names
    """

    env = {}
    for name in names:
        env[name] = ENV.get("_".join([prefix, name]))
        if env[name] is None:
            return None

    return env