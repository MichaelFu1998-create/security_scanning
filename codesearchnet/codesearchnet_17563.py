def get_date(date):
    """
    Get the date from a value that could be a date object or a string.

    :param date: The date object or string.

    :returns: The date object.
    """
    if type(date) is str:
        return datetime.strptime(date, '%Y-%m-%d').date()
    else:
        return date