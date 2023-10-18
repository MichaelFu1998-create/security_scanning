def get_cfg_value(config, section, option):
    """Get configuration value."""
    try:
        value = config[section][option]
    except KeyError:
        if (section, option) in MULTI_OPTIONS:
            return []
        else:
            return ''
    if (section, option) in MULTI_OPTIONS:
        value = split_multiline(value)
    if (section, option) in ENVIRON_OPTIONS:
        value = eval_environ(value)
    return value