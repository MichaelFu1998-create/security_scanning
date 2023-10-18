def bulkBatchDF(symbols, fields=None, range_='1m', last=10, token='', version=''):
    '''Optimized batch to fetch as much as possible at once

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
    dat = bulkBatch(symbols, fields, range_, last, token, version)
    ret = {}
    for symbol in dat:
        for field in dat[symbol]:
            if field not in ret:
                ret[field] = pd.DataFrame()

            d = dat[symbol][field]
            d = _MAPPING[field](d)
            d['symbol'] = symbol
            ret[field] = pd.concat([ret[field], d], sort=True)

    return ret