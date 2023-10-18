def format_pathname(
        pathname,
        max_length):
    """
    Format a pathname

    :param str pathname: Pathname to format
    :param int max_length: Maximum length of result pathname (> 3)
    :return: Formatted pathname
    :rtype: str
    :raises ValueError: If *max_length* is not larger than 3

    This function formats a pathname so it is not longer than *max_length*
    characters. The resulting pathname is returned. It does so by replacing
    characters at the start of the *pathname* with three dots, if necessary.
    The idea is that the end of the *pathname* is the most important part
    to be able to identify the file.
    """
    if max_length <= 3:
        raise ValueError("max length must be larger than 3")

    if len(pathname) > max_length:
        pathname = "...{}".format(pathname[-(max_length-3):])

    return pathname