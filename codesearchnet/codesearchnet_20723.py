def is_fnmatch_regex(string):
    """
    Returns True if the given string is considered a fnmatch
    regular expression, False otherwise.
    It will look for

    :param string: str

    """
    is_regex = False
    regex_chars = ['!', '*', '$']
    for c in regex_chars:
        if string.find(c) > -1:
            return True
    return is_regex