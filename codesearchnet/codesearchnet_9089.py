def get_tz(tz) -> str:
    """
    Convert tz from ticker / shorthands to timezone

    Args:
        tz: ticker or timezone shorthands

    Returns:
        str: Python timzone

    Examples:
        >>> get_tz('NY')
        'America/New_York'
        >>> get_tz(TimeZone.NY)
        'America/New_York'
        >>> get_tz('BHP AU Equity')
        'Australia/Sydney'
    """
    from xbbg.const import exch_info

    if tz is None: return DEFAULT_TZ

    to_tz = tz
    if isinstance(tz, str):
        if hasattr(TimeZone, tz):
            to_tz = getattr(TimeZone, tz)
        else:
            exch = exch_info(ticker=tz)
            if 'tz' in exch.index:
                to_tz = exch.tz

    return to_tz