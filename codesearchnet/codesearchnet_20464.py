def config_to_args(config):
    """Convert config dict to arguments list.

    :param config: Configuration dict.
    """
    result = []

    for key, value in iteritems(config):
        if value is False:
            continue

        key = '--{0}'.format(key.replace('_', '-'))

        if isinstance(value, (list, set, tuple)):
            for item in value:
                result.extend((key, smart_str(item)))
        elif value is not True:
            result.extend((key, smart_str(value)))
        else:
            result.append(key)

    return tuple(result)