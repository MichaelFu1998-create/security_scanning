def prevweekday(when, weekday, inclusive=True):
    """
    Return the date for the most recent day of the week. If inclusive is True (the default) today
    may count as the weekday we're looking for.
    """
    if isinstance(when, datetime):
        when = when.date()
    delta = weekday - when.weekday()
    if (inclusive and delta > 0) or (not inclusive and delta >= 0):
        delta -= 7
    return when + timedelta(days=delta)