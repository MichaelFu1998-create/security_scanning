def exch_info(ticker: str) -> pd.Series:
    """
    Exchange info for given ticker

    Args:
        ticker: ticker or exchange

    Returns:
        pd.Series

    Examples:
        >>> exch_info('SPY US Equity')
        tz        America/New_York
        allday      [04:00, 20:00]
        day         [09:30, 16:00]
        pre         [04:00, 09:30]
        post        [16:01, 20:00]
        dtype: object
        >>> exch_info('ES1 Index')
        tz        America/New_York
        allday      [18:00, 17:00]
        day         [08:00, 17:00]
        dtype: object
        >>> exch_info('Z 1 Index')
        tz         Europe/London
        allday    [01:00, 21:00]
        day       [01:00, 21:00]
        dtype: object
        >>> exch_info('TESTTICKER Corp').empty
        True
        >>> exch_info('US')
        tz        America/New_York
        allday      [04:00, 20:00]
        day         [09:30, 16:00]
        pre         [04:00, 09:30]
        post        [16:01, 20:00]
        dtype: object
    """
    logger = logs.get_logger(exch_info, level='debug')
    if ' ' not in ticker.strip():
        ticker = f'XYZ {ticker.strip()} Equity'
    info = param.load_info(cat='exch').get(
        market_info(ticker=ticker).get('exch', ''), dict()
    )
    if ('allday' in info) and ('day' not in info):
        info['day'] = info['allday']

    if any(req not in info for req in ['tz', 'allday', 'day']):
        logger.error(f'required exchange info cannot be found in {ticker} ...')
        return pd.Series()

    for ss in ValidSessions:
        if ss not in info: continue
        info[ss] = [param.to_hour(num=s) for s in info[ss]]

    return pd.Series(info)