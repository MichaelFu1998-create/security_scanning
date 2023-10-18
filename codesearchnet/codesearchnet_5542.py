def chartDF(symbol, timeframe='1m', date=None, token='', version=''):
    '''Historical price/volume data, daily and intraday

    https://iexcloud.io/docs/api/#historical-prices
    Data Schedule
    1d: -9:30-4pm ET Mon-Fri on regular market trading days
        -9:30-1pm ET on early close trading days
    All others:
        -Prior trading day available after 4am ET Tue-Sat

    Args:
        symbol (string); Ticker to request
        timeframe (string); Timeframe to request e.g. 1m
        date (datetime): date, if requesting intraday
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: result
    '''
    c = chart(symbol, timeframe, date, token, version)
    df = pd.DataFrame(c)
    _toDatetime(df)
    if timeframe is not None and timeframe != '1d':
        _reindex(df, 'date')
    else:
        if not df.empty:
            df.set_index(['date', 'minute'], inplace=True)
        else:
            return pd.DataFrame()
    return df