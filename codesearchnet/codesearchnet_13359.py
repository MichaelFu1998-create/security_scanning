def datetime_utc_to_local(utc):
    """
    An ugly hack to convert naive :std:`datetime.datetime` object containing
    UTC time to a naive :std:`datetime.datetime` object with local time.
    It seems standard Python 2.3 library doesn't provide any better way to
    do that.
    """
    # pylint: disable-msg=C0103
    ts = time.time()
    cur = datetime.datetime.fromtimestamp(ts)
    cur_utc = datetime.datetime.utcfromtimestamp(ts)

    offset = cur - cur_utc
    t = utc

    d = datetime.timedelta(hours = 2)
    while d > _MINUTE:
        local = t + offset
        tm = local.timetuple()
        tm = tm[0:8] + (0, )
        ts = time.mktime(tm)
        u = datetime.datetime.utcfromtimestamp(ts)
        diff = u - utc
        if diff < _MINUTE and diff > -_MINUTE:
            break
        if diff > _NULLDELTA:
            offset -= d
        else:
            offset += d
        d //= 2
    return local