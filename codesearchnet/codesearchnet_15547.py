def pc_or_float(s):
    """ Utility function to process strings that contain either percentiles or floats
    args:
        str: s
    returns:
       float
    """
    if isinstance(s, string_types) and '%' in s:
        return float(s.strip('%')) / 100.0
    return float(s)