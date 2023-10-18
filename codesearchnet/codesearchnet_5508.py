def calendar(type='holiday', direction='next', last=1, startDate=None, token='', version=''):
    '''This call allows you to fetch a number of trade dates or holidays from a given date. For example, if you want the next trading day, you would call /ref-data/us/dates/trade/next/1.

    https://iexcloud.io/docs/api/#u-s-exchanges
    8am, 9am, 12pm, 1pm UTC daily

    Args:
        type (string); "holiday" or "trade"
        direction (string); "next" or "last"
        last (int); number to move in direction
        startDate (date); start date for next or last, YYYYMMDD
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    if startDate:
        startDate = _strOrDate(startDate)
        return _getJson('ref-data/us/dates/{type}/{direction}/{last}/{date}'.format(type=type, direction=direction, last=last, date=startDate), token, version)
    return _getJson('ref-data/us/dates/' + type + '/' + direction + '/' + str(last), token, version)