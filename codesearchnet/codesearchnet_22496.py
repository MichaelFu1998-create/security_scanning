def value_to_bool(config_val, evar):
    """
    Massages the 'true' and 'false' strings to bool equivalents.

    :param str config_val: The env var value.
    :param EnvironmentVariable evar: The EVar object we are validating
        a value for.
    :rtype: bool
    :return: True or False, depending on the value.
    """
    if not config_val:
        return False
    if config_val.strip().lower() == 'true':
        return True
    else:
        return False