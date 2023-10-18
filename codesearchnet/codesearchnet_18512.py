def _validate(config):
    """ Config validation
    Raises:
        KeyError        on missing mandatory key
        SyntaxError     on invalid key
        ValueError      on invalid value for key
    :param config: {dict} config to validate
    :return: None
    """
    for mandatory_key in _mandatory_keys:
        if mandatory_key not in config:
            raise KeyError(mandatory_key)
    for key in config.keys():
        if key not in _mandatory_keys and key not in _optional_keys:
            raise SyntaxError(key)
        if not isinstance(config[key], _default_config[key].__class__):
            raise ValueError(key)