def summary(date=None, token='', version=''):
    '''https://iexcloud.io/docs/api/#stats-historical-summary

    Args:
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    if date:
        if isinstance(date, str):
            return _getJson('stats/historical?date=' + date, token, version)
        elif isinstance(date, datetime):
            return _getJson('stats/historical?date=' + date.strftime('%Y%m'), token, version)
        else:
            raise PyEXception("Can't handle type : %s" % str(type(date)), token, version)
    return _getJson('stats/historical', token, version)