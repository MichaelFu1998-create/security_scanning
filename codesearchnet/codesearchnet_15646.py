def dict_format_type(d, source, formatter, include_list=True):
    """
    Replace the values of a dict with certain type to other values
    :param d: the dictionary
    :param source: the source type, e.g., int
    :param formatter: the formatter method, e.g., return the string format of an int
    :param include_list: whether list should be formatted, otherwise list will be considered as source type
    :return: formatted dictionary
    """
    if not isinstance(d, dict):
        if isinstance(d, source):
            return formatter(d)
        else:
            return d
    else:
        dd = dict()
        for key, value in d.items():
            if include_list and isinstance(value, list):
                dd[key] = [dict_format_type(i, source, formatter) for i in value]
            elif isinstance(value, dict):
                dd[key] = dict_format_type(value, source, formatter)
            elif isinstance(value, source):
                dd[key] = formatter(value)
            else:
                dd[key] = value
        return dd