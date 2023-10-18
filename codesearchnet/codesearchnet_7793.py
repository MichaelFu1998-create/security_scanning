def _convert_config_to_stdin(config, parser):
    """Convert config options to stdin args.

    Especially boolean values, for more information
    @see https://docs.python.org/3.4/library/configparser.html#supported-datatypes
    """
    keys_empty_values_not_pass = (
        '--extra-settings', '--languages', '--requirements', '--template', '--timezone')
    args = []
    for key, val in config.items(SECTION):
        keyp = '--{0}'.format(key)
        action = parser._option_string_actions[keyp]

        if action.const:
            try:
                if config.getboolean(SECTION, key):
                    args.append(keyp)
            except ValueError:
                args.extend([keyp, val])  # Pass it as is to get the error from ArgumentParser.
        elif any([i for i in keys_empty_values_not_pass if i in action.option_strings]):
            # Some keys with empty values shouldn't be passed into args to use their defaults
            # from ArgumentParser.
            if val != '':
                args.extend([keyp, val])
        else:
            args.extend([keyp, val])

    return args