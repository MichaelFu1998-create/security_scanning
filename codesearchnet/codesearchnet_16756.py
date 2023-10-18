def parse_option_settings(option_settings):
    """
    Parses option_settings as they are defined in the configuration file
    """
    ret = []
    for namespace, params in list(option_settings.items()):
        for key, value in list(params.items()):
            ret.append((namespace, key, value))
    return ret