def determine_type(x):
    """Determine the type of x"""
    types = (int, float, str)
    _type = filter(lambda a: is_type(a, x), types)[0]
    return _type(x)