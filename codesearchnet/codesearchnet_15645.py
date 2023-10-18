def dict_flatten(d):
    """
    Replace nested dict keys to underscore-connected keys
    :param d: the dictionary
    :return: flattened dictionary
    """
    if type(d) != dict:
        return d
    else:
        dd = dict()
        for key, value in d.items():
            if type(value) == dict:
                for k, v in value.items():
                    dd[key + '_' + k] = dict_flatten(v)
            else:
                dd[key] = value
        return dd