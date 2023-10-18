def datetime_iso_format(date):
    """
    Return an ISO-8601 representation of a datetime object.
    """
    return "{0:0>4}-{1:0>2}-{2:0>2}T{3:0>2}:{4:0>2}:{5:0>2}Z".format(
        date.year, date.month, date.day, date.hour,
        date.minute, date.second)