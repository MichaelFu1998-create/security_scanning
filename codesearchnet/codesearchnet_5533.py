def batchDF(symbols, fields=None, range_='1m', last=10, token='', version=''):
    '''Batch several data requests into one invocation

    https://iexcloud.io/docs/api/#batch-requests


    Args:
        symbols (list); List of tickers to request
        fields (list); List of fields to request
        range_ (string); Date range for chart
        last (int);
        token (string); Access token
        version (string); API version

    Returns:
        DataFrame: results in json
    '''
    x = batch(symbols, fields, range_, last, token, version)

    ret = {}

    if isinstance(symbols, str):
        for field in x.keys():
            ret[field] = _MAPPING[field](x[field])
    else:
        for symbol in x.keys():
            for field in x[symbol].keys():
                if field not in ret:
                    ret[field] = pd.DataFrame()

                dat = x[symbol][field]
                dat = _MAPPING[field](dat)
                dat['symbol'] = symbol

                ret[field] = pd.concat([ret[field], dat], sort=True)
    return ret