def hist_file(ticker: str, dt, typ='TRADE') -> str:
    """
    Data file location for Bloomberg historical data

    Args:
        ticker: ticker name
        dt: date
        typ: [TRADE, BID, ASK, BID_BEST, ASK_BEST, BEST_BID, BEST_ASK]

    Returns:
        file location

    Examples:
        >>> os.environ['BBG_ROOT'] = ''
        >>> hist_file(ticker='ES1 Index', dt='2018-08-01') == ''
        True
        >>> os.environ['BBG_ROOT'] = '/data/bbg'
        >>> hist_file(ticker='ES1 Index', dt='2018-08-01')
        '/data/bbg/Index/ES1 Index/TRADE/2018-08-01.parq'
    """
    data_path = os.environ.get(assist.BBG_ROOT, '').replace('\\', '/')
    if not data_path: return ''
    asset = ticker.split()[-1]
    proper_ticker = ticker.replace('/', '_')
    cur_dt = pd.Timestamp(dt).strftime('%Y-%m-%d')
    return f'{data_path}/{asset}/{proper_ticker}/{typ}/{cur_dt}.parq'