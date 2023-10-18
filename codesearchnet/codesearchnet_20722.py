def is_regex(string):
    """
    TODO: improve this!

    Returns True if the given string is considered a regular expression,
    False otherwise.
    It will be considered a regex if starts with a non alphabetic character
    and then correctly compiled by re.compile

    :param string: str

    """
    is_regex = False
    regex_chars = ['\\', '(', '+', '^', '$']
    for c in regex_chars:
        if string.find(c) > -1:
            return is_valid_regex(string)
    return is_regex