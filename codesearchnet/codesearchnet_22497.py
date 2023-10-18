def validate_is_not_none(config_val, evar):
    """
    If the value is ``None``, fail validation.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :raises: ValueError if the config value is None.
    """
    if config_val is None:
        raise ValueError(
            "Value for environment variable '{evar_name}' can't "
            "be empty.".format(evar_name=evar.name))
    return config_val