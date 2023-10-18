def format_val(val):
    """
    Returns val as integer or as escaped string according to its value
    :param val: any value
    :return: formatted string
    """
    val = text_type(val)
    if val.isdigit():
        return int(val)
    else:
        return '\'{0}\''.format(val)