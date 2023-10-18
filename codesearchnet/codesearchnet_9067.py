def market_timing(ticker, dt, timing='EOD', tz='local') -> str:
    """
    Market close time for ticker

    Args:
        ticker: ticker name
        dt: date
        timing: [EOD (default), BOD]
        tz: conversion to timezone

    Returns:
        str: date & time

    Examples:
        >>> market_timing('7267 JT Equity', dt='2018-09-10')
        '2018-09-10 14:58'
        >>> market_timing('7267 JT Equity', dt='2018-09-10', tz=timezone.TimeZone.NY)
        '2018-09-10 01:58:00-04:00'
        >>> market_timing('7267 JT Equity', dt='2018-01-10', tz='NY')
        '2018-01-10 00:58:00-05:00'
        >>> market_timing('7267 JT Equity', dt='2018-09-10', tz='SPX Index')
        '2018-09-10 01:58:00-04:00'
        >>> market_timing('8035 JT Equity', dt='2018-09-10', timing='BOD')
        '2018-09-10 09:01'
        >>> market_timing('Z 1 Index', dt='2018-09-10', timing='FINISHED')
        '2018-09-10 21:00'
        >>> market_timing('TESTTICKER Corp', dt='2018-09-10')
        ''
    """
    logger = logs.get_logger(market_timing)
    exch = pd.Series(exch_info(ticker=ticker))
    if any(req not in exch.index for req in ['tz', 'allday', 'day']):
        logger.error(f'required exchange info cannot be found in {ticker} ...')
        return ''

    mkt_time = {
        'BOD': exch.day[0], 'FINISHED': exch.allday[-1]
    }.get(timing, exch.day[-1])

    cur_dt = pd.Timestamp(str(dt)).strftime('%Y-%m-%d')
    if tz == 'local':
        return f'{cur_dt} {mkt_time}'

    return timezone.tz_convert(f'{cur_dt} {mkt_time}', to_tz=tz, from_tz=exch.tz)