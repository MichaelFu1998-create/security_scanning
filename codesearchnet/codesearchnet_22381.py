def strip_codes(s: Any) -> str:
    """ Strip all color codes from a string.
        Returns empty string for "falsey" inputs.
    """
    return codepat.sub('', str(s) if (s or (s == 0)) else '')