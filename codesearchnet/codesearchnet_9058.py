def active_futures(ticker: str, dt) -> str:
    """
    Active futures contract

    Args:
        ticker: futures ticker, i.e., ESA Index, Z A Index, CLA Comdty, etc.
        dt: date

    Returns:
        str: ticker name
    """
    t_info = ticker.split()
    prefix, asset = ' '.join(t_info[:-1]), t_info[-1]
    info = const.market_info(f'{prefix[:-1]}1 {asset}')

    f1, f2 = f'{prefix[:-1]}1 {asset}', f'{prefix[:-1]}2 {asset}'
    fut_2 = fut_ticker(gen_ticker=f2, dt=dt, freq=info['freq'])
    fut_1 = fut_ticker(gen_ticker=f1, dt=dt, freq=info['freq'])

    fut_tk = bdp(tickers=[fut_1, fut_2], flds='Last_Tradeable_Dt', cache=True)

    if pd.Timestamp(dt).month < pd.Timestamp(fut_tk.last_tradeable_dt[0]).month: return fut_1

    d1 = bdib(ticker=f1, dt=dt)
    d2 = bdib(ticker=f2, dt=dt)

    return fut_1 if d1[f1].volume.sum() > d2[f2].volume.sum() else fut_2