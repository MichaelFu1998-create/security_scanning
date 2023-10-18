def match_part(string, part):
    """Raise an exception if string doesn't match a part's regex

    :param string: str
    :param part: a key in the PARTS dict
    :raises: ValueError, TypeError
    """
    if not string or not re.match('^(' + PARTS[part] + ')$', string):
        raise ValueError('{} should match {}'.format(part, PARTS[part]))