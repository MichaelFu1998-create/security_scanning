def weekday(when, weekday, start=mon):
    """Return the date for the day of this week."""
    if isinstance(when, datetime):
        when = when.date()

    today = when.weekday()
    delta = weekday - today
    if weekday < start and today >= start:
        delta += 7
    elif weekday >= start and today < start:
        delta -= 7
    return when + timedelta(days=delta)