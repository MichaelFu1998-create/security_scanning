def intraday(ticker, dt, session='', **kwargs) -> pd.DataFrame:
    """
    Bloomberg intraday bar data within market session

    Args:
        ticker: ticker
        dt: date
        session: examples include
                 day_open_30, am_normal_30_30, day_close_30, allday_exact_0930_1000
        **kwargs:
            ref: reference ticker or exchange for timezone
            keep_tz: if keep tz if reference ticker / exchange is given
            start_time: start time
            end_time: end time
            typ: [TRADE, BID, ASK, BID_BEST, ASK_BEST, BEST_BID, BEST_ASK]

    Returns:
        pd.DataFrame
    """
    from xbbg.core import intervals

    cur_data = bdib(ticker=ticker, dt=dt, typ=kwargs.get('typ', 'TRADE'))
    if cur_data.empty: return pd.DataFrame()

    fmt = '%H:%M:%S'
    ss = intervals.SessNA
    ref = kwargs.get('ref', None)
    exch = pd.Series() if ref is None else const.exch_info(ticker=ref)
    if session: ss = intervals.get_interval(
        ticker=kwargs.get('ref', ticker), session=session
    )

    start_time = kwargs.get('start_time', None)
    end_time = kwargs.get('end_time', None)
    if ss != intervals.SessNA:
        start_time = pd.Timestamp(ss.start_time).strftime(fmt)
        end_time = pd.Timestamp(ss.end_time).strftime(fmt)

    if start_time and end_time:
        kw = dict(start_time=start_time, end_time=end_time)
        if not exch.empty:
            cur_tz = cur_data.index.tz
            res = cur_data.tz_convert(exch.tz).between_time(**kw)
            if kwargs.get('keep_tz', False):
                res = res.tz_convert(cur_tz)
            return pd.DataFrame(res)
        return pd.DataFrame(cur_data.between_time(**kw))

    return cur_data