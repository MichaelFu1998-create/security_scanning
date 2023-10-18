def is_variable(value):
    """ Check if string is LESS variable
    args:
        value (str): string
    returns:
        bool
    """
    if isinstance(value, string_types):
        return (value.startswith('@') or value.startswith('-@'))
    elif isinstance(value, tuple):
        value = ''.join(value)
        return (value.startswith('@') or value.startswith('-@'))
    return False