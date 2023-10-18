def cur_time(typ='date', tz=DEFAULT_TZ) -> (datetime.date, str):
    """
    Current time

    Args:
        typ: one of ['date', 'time', 'time_path', 'raw', '']
        tz: timezone

    Returns:
        relevant current time or date

    Examples:
        >>> cur_dt = pd.Timestamp('now')
        >>> cur_time(typ='date') == cur_dt.strftime('%Y-%m-%d')
        True
        >>> cur_time(typ='time') == cur_dt.strftime('%Y-%m-%d %H:%M:%S')
        True
        >>> cur_time(typ='time_path') == cur_dt.strftime('%Y-%m-%d/%H-%M-%S')
        True
        >>> isinstance(cur_time(typ='raw', tz='Europe/London'), pd.Timestamp)
        True
        >>> cur_time(typ='') == cur_dt.date()
        True
    """
    dt = pd.Timestamp('now', tz=tz)

    if typ == 'date': return dt.strftime('%Y-%m-%d')
    if typ == 'time': return dt.strftime('%Y-%m-%d %H:%M:%S')
    if typ == 'time_path': return dt.strftime('%Y-%m-%d/%H-%M-%S')
    if typ == 'raw': return dt

    return dt.date()