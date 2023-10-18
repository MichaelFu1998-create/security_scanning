def format_time_point(
        time_point_string):

    """
    :param str time_point_string: String representation of a time point
        to format
    :return: Formatted time point
    :rtype: str
    :raises ValueError: If *time_point_string* is not formatted by
        dateutil.parser.parse

    See :py:meth:`datetime.datetime.isoformat` function for supported formats.
    """
    time_point = dateutil.parser.parse(time_point_string)

    if not is_aware(time_point):
        time_point = make_aware(time_point)

    time_point = local_time_point(time_point)

    return time_point.strftime("%Y-%m-%dT%H:%M:%S")