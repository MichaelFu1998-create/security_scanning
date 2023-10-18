def _build_dict_from_key_value(keys_and_values):
    """Return a dict from a list of key=value pairs
    """
    key_dict = {}
    for key_value in keys_and_values:
        if '=' not in key_value:
            raise GhostError('Pair {0} is not of `key=value` format'.format(
                key_value))
        key, value = key_value.split('=', 1)
        key_dict.update({str(key): str(value)})
    return key_dict