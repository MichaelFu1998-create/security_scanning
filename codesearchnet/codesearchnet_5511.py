def holidaysDF(direction='next', last=1, startDate=None, token='', version=''):
    '''This call allows you to fetch a number of trade dates or holidays from a given date. For example, if you want the next trading day, you would call /ref-data/us/dates/trade/next/1.

    https://iexcloud.io/docs/api/#u-s-exchanges
    8am, 9am, 12pm, 1pm UTC daily

    Args:
        direction (string); "next" or "last"
        last (int); number to move in direction
        startDate (date); start date for next or last, YYYYMMDD
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    return calendarDF('holiday', direction, last, startDate, token, version)