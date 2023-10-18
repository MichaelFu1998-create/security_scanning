def format_uuid(
        uuid,
        max_length=10):
    """
    Format a UUID string

    :param str uuid: UUID to format
    :param int max_length: Maximum length of result string (> 3)
    :return: Formatted UUID
    :rtype: str
    :raises ValueError: If *max_length* is not larger than 3

    This function formats a UUID so it is not longer than *max_length*
    characters. The resulting string is returned. It does so by replacing
    characters at the end of the *uuid* with three dots, if necessary.
    The idea is that the start of the *uuid* is the most important part
    to be able to identify the related entity.

    The default *max_length* is 10, which will result in a string
    containing the first 7 characters of the *uuid* passed in. Most of
    the time, such a string is still unique within a collection of UUIDs.
    """
    if max_length <= 3:
        raise ValueError("max length must be larger than 3")

    if len(uuid) > max_length:
        uuid = "{}...".format(uuid[0:max_length-3])

    return uuid