def truncate(when, unit, week_start=mon):
    """Return the datetime truncated to the precision of the provided unit."""
    if is_datetime(when):
        if unit == millisecond:
            return when.replace(microsecond=int(round(when.microsecond / 1000.0)) * 1000)
        elif unit == second:
            return when.replace(microsecond=0)
        elif unit == minute:
            return when.replace(second=0, microsecond=0)
        elif unit == hour:
            return when.replace(minute=0, second=0, microsecond=0)
        elif unit == day:
            return when.replace(hour=0, minute=0, second=0, microsecond=0)
        elif unit == week:
            weekday = prevweekday(when, week_start)
            return when.replace(year=weekday.year, month=weekday.month, day=weekday.day,
                                hour=0, minute=0, second=0, microsecond=0)
        elif unit == month:
            return when.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif unit == year:
            return when.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif is_date(when):
        if unit == week:
            return prevweekday(when, week_start)
        elif unit == month:
            return when.replace(day=1)
        elif unit == year:
            return when.replace(month=1, day=1)
    elif is_time(when):
        if unit == millisecond:
            return when.replace(microsecond=int(when.microsecond / 1000.0) * 1000)
        elif unit == second:
            return when.replace(microsecond=0)
        elif unit == minute:
            return when.replace(second=0, microsecond=0)
    return when