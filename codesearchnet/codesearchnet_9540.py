def validate_values(config, values):
    """
    Validate whether value is found in config and has the right type.

    Parameters
    ----------
    config : dict
        configuration dictionary
    values : list
        list of (str, type) tuples of values and value types expected in config

    Returns
    -------
    True if config is valid.

    Raises
    ------
    Exception if value is not found or has the wrong type.
    """
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    for value, vtype in values:
        if value not in config:
            raise ValueError("%s not given" % value)
        if not isinstance(config[value], vtype):
            raise TypeError("%s must be %s" % (value, vtype))
    return True