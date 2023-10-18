def get_interval(ticker, session) -> Session:
    """
    Get interval from defined session

    Args:
        ticker: ticker
        session: session

    Returns:
        Session of start_time and end_time

    Examples:
        >>> get_interval('005490 KS Equity', 'day_open_30')
        Session(start_time='09:00', end_time='09:30')
        >>> get_interval('005490 KS Equity', 'day_normal_30_20')
        Session(start_time='09:31', end_time='15:00')
        >>> get_interval('005490 KS Equity', 'day_close_20')
        Session(start_time='15:01', end_time='15:20')
        >>> get_interval('700 HK Equity', 'am_open_30')
        Session(start_time='09:30', end_time='10:00')
        >>> get_interval('700 HK Equity', 'am_normal_30_30')
        Session(start_time='10:01', end_time='11:30')
        >>> get_interval('700 HK Equity', 'am_close_30')
        Session(start_time='11:31', end_time='12:00')
        >>> get_interval('ES1 Index', 'day_exact_2130_2230')
        Session(start_time=None, end_time=None)
        >>> get_interval('ES1 Index', 'allday_exact_2130_2230')
        Session(start_time='21:30', end_time='22:30')
        >>> get_interval('ES1 Index', 'allday_exact_2130_0230')
        Session(start_time='21:30', end_time='02:30')
        >>> get_interval('AMLP US', 'day_open_30')
        Session(start_time=None, end_time=None)
        >>> get_interval('7974 JP Equity', 'day_normal_180_300') is SessNA
        True
        >>> get_interval('Z 1 Index', 'allday_normal_30_30')
        Session(start_time='01:31', end_time='20:30')
        >>> get_interval('GBP Curncy', 'day')
        Session(start_time='17:02', end_time='17:00')
    """
    if '_' not in session:
        session = f'{session}_normal_0_0'
    interval = Intervals(ticker=ticker)
    ss_info = session.split('_')
    return getattr(interval, f'market_{ss_info.pop(1)}')(*ss_info)