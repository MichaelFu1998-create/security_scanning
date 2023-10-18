def daily(date=None, last='', token='', version=''):
    '''https://iexcloud.io/docs/api/#stats-historical-daily

    Args:
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    if date:
        date = _strOrDate(date)
        return _getJson('stats/historical/daily?date=' + date, token, version)
    elif last:
        return _getJson('stats/historical/daily?last=' + last, token, version)
    return _getJson('stats/historical/daily', token, version)