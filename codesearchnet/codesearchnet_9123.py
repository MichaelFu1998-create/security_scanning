def capitalcase(string):
    """Convert string into capital case.
    First letters will be uppercase.

    Args:
        string: String to convert.

    Returns:
        string: Capital case string.

    """

    string = str(string)
    if not string:
        return string
    return uppercase(string[0]) + string[1:]