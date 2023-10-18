def set_cfg_value(config, section, option, value):
    """Set configuration value."""
    if isinstance(value, list):
        value = '\n'.join(value)
    config[section][option] = value