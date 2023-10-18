def str_time_to_day_seconds(time):
    """
    Converts time strings to integer seconds
    :param time: %H:%M:%S string
    :return: integer seconds
    """
    t = str(time).split(':')
    seconds = int(t[0]) * 3600 + int(t[1]) * 60 + int(t[2])
    return seconds