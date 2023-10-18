def value_to_python_log_level(config_val, evar):
    """
    Convert an evar value into a Python logging level constant.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :return: A validated string.
    :raises: ValueError if the log level is invalid.
    """
    if not config_val:
        config_val = evar.default_val
    config_val = config_val.upper()
    # noinspection PyProtectedMember
    return logging._checkLevel(config_val)