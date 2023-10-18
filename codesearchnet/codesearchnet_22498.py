def validate_is_boolean_true(config_val, evar):
    """
    Make sure the value evaluates to boolean True.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :raises: ValueError if the config value evaluates to boolean False.
    """
    if config_val is None:
        raise ValueError(
            "Value for environment variable '{evar_name}' can't "
            "be empty.".format(evar_name=evar.name))
    return config_val