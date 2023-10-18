def save_intraday(data: pd.DataFrame, ticker: str, dt, typ='TRADE'):
    """
    Check whether data is done for the day and save

    Args:
        data: data
        ticker: ticker
        dt: date
        typ: [TRADE, BID, ASK, BID_BEST, ASK_BEST, BEST_BID, BEST_ASK]

    Examples:
        >>> os.environ['BBG_ROOT'] = 'xbbg/tests/data'
        >>> sample = pd.read_parquet('xbbg/tests/data/aapl.parq')
        >>> save_intraday(sample, 'AAPL US Equity', '2018-11-02')
        >>> # Invalid exchange
        >>> save_intraday(sample, 'AAPL XX Equity', '2018-11-02')
        >>> # Invalid empty data
        >>> save_intraday(pd.DataFrame(), 'AAPL US Equity', '2018-11-02')
        >>> # Invalid date - too close
        >>> cur_dt = utils.cur_time()
        >>> save_intraday(sample, 'AAPL US Equity', cur_dt)
    """
    cur_dt = pd.Timestamp(dt).strftime('%Y-%m-%d')
    logger = logs.get_logger(save_intraday, level='debug')
    info = f'{ticker} / {cur_dt} / {typ}'
    data_file = hist_file(ticker=ticker, dt=dt, typ=typ)
    if not data_file: return

    if data.empty:
        logger.warning(f'data is empty for {info} ...')
        return

    exch = const.exch_info(ticker=ticker)
    if exch.empty: return

    end_time = pd.Timestamp(
        const.market_timing(ticker=ticker, dt=dt, timing='FINISHED')
    ).tz_localize(exch.tz)
    now = pd.Timestamp('now', tz=exch.tz) - pd.Timedelta('1H')

    if end_time > now:
        logger.debug(f'skip saving cause market close ({end_time}) < now - 1H ({now}) ...')
        return

    logger.info(f'saving data to {data_file} ...')
    files.create_folder(data_file, is_file=True)
    data.to_parquet(data_file)