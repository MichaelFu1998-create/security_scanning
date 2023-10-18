def is_float(value):
    """ Is value float
    args:
        value (str): string
    returns:
        bool
    """
    if not is_int(value):
        try:
            float(str(value))
            return True
        except (ValueError, TypeError):
            pass
    return False