def is_color(value):
    """ Is string CSS color
    args:
        value (str): string
    returns:
        bool
    """
    if not value or not isinstance(value, string_types):
        return False
    if value[0] == '#' and len(value) in [4, 5, 7, 9]:
        try:
            int(value[1:], 16)
            return True
        except ValueError:
            pass
    return False