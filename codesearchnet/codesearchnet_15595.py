def timestring_to_datetime(timestring):
    """
    Convert an ISO formated date and time string to a datetime object.

    :param str timestring: String with date and time in ISO format.
    :rtype: datetime
    :return: datetime object
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UnicodeWarning)
        result = dateutil_parser(timestring)

    return result