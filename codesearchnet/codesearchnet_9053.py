def bdh(
        tickers, flds=None, start_date=None, end_date='today', adjust=None, **kwargs
) -> pd.DataFrame:
    """
    Bloomberg historical data

    Args:
        tickers: ticker(s)
        flds: field(s)
        start_date: start date
        end_date: end date - default today
        adjust: `all`, `dvd`, `normal`, `abn` (=abnormal), `split`, `-` or None
                exact match of above words will adjust for corresponding events
                Case 0: `-` no adjustment for dividend or split
                Case 1: `dvd` or `normal|abn` will adjust for all dividends except splits
                Case 2: `adjust` will adjust for splits and ignore all dividends
                Case 3: `all` == `dvd|split` == adjust for all
                Case 4: None == Bloomberg default OR use kwargs
        **kwargs: overrides

    Returns:
        pd.DataFrame

    Examples:
        >>> res = bdh(
        ...     tickers='VIX Index', flds=['High', 'Low', 'Last_Price'],
        ...     start_date='2018-02-05', end_date='2018-02-07',
        ... ).round(2).transpose()
        >>> res.index.name = None
        >>> res.columns.name = None
        >>> res
                              2018-02-05  2018-02-06  2018-02-07
        VIX Index High             38.80       50.30       31.64
                  Low              16.80       22.42       21.17
                  Last_Price       37.32       29.98       27.73
        >>> bdh(
        ...     tickers='AAPL US Equity', flds='Px_Last',
        ...     start_date='20140605', end_date='20140610', adjust='-'
        ... ).round(2)
        ticker     AAPL US Equity
        field             Px_Last
        2014-06-05         647.35
        2014-06-06         645.57
        2014-06-09          93.70
        2014-06-10          94.25
        >>> bdh(
        ...     tickers='AAPL US Equity', flds='Px_Last',
        ...     start_date='20140606', end_date='20140609',
        ...     CshAdjNormal=False, CshAdjAbnormal=False, CapChg=False,
        ... ).round(2)
        ticker     AAPL US Equity
        field             Px_Last
        2014-06-06         645.57
        2014-06-09          93.70
    """
    logger = logs.get_logger(bdh, level=kwargs.pop('log', logs.LOG_LEVEL))

    # Dividend adjustments
    if isinstance(adjust, str) and adjust:
        if adjust == 'all':
            kwargs['CshAdjNormal'] = True
            kwargs['CshAdjAbnormal'] = True
            kwargs['CapChg'] = True
        else:
            kwargs['CshAdjNormal'] = 'normal' in adjust or 'dvd' in adjust
            kwargs['CshAdjAbnormal'] = 'abn' in adjust or 'dvd' in adjust
            kwargs['CapChg'] = 'split' in adjust

    con, _ = create_connection()
    elms = assist.proc_elms(**kwargs)
    ovrds = assist.proc_ovrds(**kwargs)

    if isinstance(tickers, str): tickers = [tickers]
    if flds is None: flds = ['Last_Price']
    if isinstance(flds, str): flds = [flds]
    e_dt = utils.fmt_dt(end_date, fmt='%Y%m%d')
    if start_date is None:
        start_date = pd.Timestamp(e_dt) - relativedelta(months=3)
    s_dt = utils.fmt_dt(start_date, fmt='%Y%m%d')

    logger.info(
        f'loading historical data from Bloomberg:\n'
        f'{assist.info_qry(tickers=tickers, flds=flds)}'
    )

    logger.debug(
        f'\nflds={flds}\nelms={elms}\novrds={ovrds}\nstart_date={s_dt}\nend_date={e_dt}'
    )
    res = con.bdh(
        tickers=tickers, flds=flds, elms=elms, ovrds=ovrds, start_date=s_dt, end_date=e_dt
    )
    res.index.name = None
    if (len(flds) == 1) and kwargs.get('keep_one', False):
        return res.xs(flds[0], axis=1, level=1)
    return res