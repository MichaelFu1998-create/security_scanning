def clean_strings(iterable):
    """
    Take a list of strings and clear whitespace 
    on each one. If a value in the list is not a 
    string pass it through untouched.

    Args:
        iterable: mixed list

    Returns: 
        mixed list
    """
    retval = []
    for val in iterable:
        try:
            retval.append(val.strip())
        except(AttributeError):
            retval.append(val)
    return retval