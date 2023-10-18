def bdib(ticker, dt, typ='TRADE', **kwargs) -> pd.DataFrame:
    """
    Bloomberg intraday bar data

    Args:
        ticker: ticker name
        dt: date to download
        typ: [TRADE, BID, ASK, BID_BEST, ASK_BEST, BEST_BID, BEST_ASK]
        **kwargs:
            batch: whether is batch process to download data
            log: level of logs

    Returns:
        pd.DataFrame
    """
    from xbbg.core import missing

    logger = logs.get_logger(bdib, level=kwargs.pop('log', logs.LOG_LEVEL))

    t_1 = pd.Timestamp('today').date() - pd.Timedelta('1D')
    whole_day = pd.Timestamp(dt).date() < t_1
    batch = kwargs.pop('batch', False)
    if (not whole_day) and batch:
        logger.warning(f'querying date {t_1} is too close, ignoring download ...')
        return pd.DataFrame()

    cur_dt = pd.Timestamp(dt).strftime('%Y-%m-%d')
    asset = ticker.split()[-1]
    info_log = f'{ticker} / {cur_dt} / {typ}'

    if asset in ['Equity', 'Curncy', 'Index', 'Comdty']:
        exch = const.exch_info(ticker=ticker)
        if exch.empty: return pd.DataFrame()
    else:
        logger.error(f'unknown asset type: {asset}')
        return pd.DataFrame()

    time_fmt = '%Y-%m-%dT%H:%M:%S'
    time_idx = pd.DatetimeIndex([
        f'{cur_dt} {exch.allday[0]}', f'{cur_dt} {exch.allday[-1]}']
    ).tz_localize(exch.tz).tz_convert(DEFAULT_TZ).tz_convert('UTC')
    if time_idx[0] > time_idx[1]: time_idx -= pd.TimedeltaIndex(['1D', '0D'])

    q_tckr = ticker
    if exch.get('is_fut', False):
        if 'freq' not in exch:
            logger.error(f'[freq] missing in info for {info_log} ...')

        is_sprd = exch.get('has_sprd', False) and (len(ticker[:-1]) != exch['tickers'][0])
        if not is_sprd:
            q_tckr = fut_ticker(gen_ticker=ticker, dt=dt, freq=exch['freq'])
            if q_tckr == '':
                logger.error(f'cannot find futures ticker for {ticker} ...')
                return pd.DataFrame()

    info_log = f'{q_tckr} / {cur_dt} / {typ}'
    miss_kw = dict(ticker=ticker, dt=dt, typ=typ, func='bdib')
    cur_miss = missing.current_missing(**miss_kw)
    if cur_miss >= 2:
        if batch: return pd.DataFrame()
        logger.info(f'{cur_miss} trials with no data {info_log}')
        return pd.DataFrame()

    logger.info(f'loading data from Bloomberg: {info_log} ...')
    con, _ = create_connection()
    try:
        data = con.bdib(
            ticker=q_tckr, event_type=typ, interval=1,
            start_datetime=time_idx[0].strftime(time_fmt),
            end_datetime=time_idx[1].strftime(time_fmt),
        )
    except KeyError:
        # Ignores missing data errors from pdblp library
        # Warning msg will be displayed later
        data = pd.DataFrame()

    if not isinstance(data, pd.DataFrame):
        raise ValueError(f'unknown output format: {type(data)}')

    if data.empty:
        logger.warning(f'no data for {info_log} ...')
        missing.update_missing(**miss_kw)
        return pd.DataFrame()

    data = data.tz_localize('UTC').tz_convert(exch.tz)
    storage.save_intraday(data=data, ticker=ticker, dt=dt, typ=typ)

    return pd.DataFrame() if batch else assist.format_intraday(data=data, ticker=ticker)