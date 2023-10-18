def bds(tickers, flds, **kwargs):
    """
    Bloomberg block data

    Args:
        tickers: ticker(s)
        flds: field(s)
        **kwargs: other overrides for query
          -> raw: raw output from `pdbdp` library, default False

    Returns:
        pd.DataFrame: block data

    Examples:
        >>> import os
        >>>
        >>> pd.options.display.width = 120
        >>> s_dt, e_dt = '20180301', '20181031'
        >>> dvd = bds(
        ...     'NVDA US Equity', 'DVD_Hist_All',
        ...     DVD_Start_Dt=s_dt, DVD_End_Dt=e_dt, raw=True,
        ... )
        >>> dvd.loc[:, ['ticker', 'name', 'value']].head(8)
                   ticker                name         value
        0  NVDA US Equity       Declared Date    2018-08-16
        1  NVDA US Equity             Ex-Date    2018-08-29
        2  NVDA US Equity         Record Date    2018-08-30
        3  NVDA US Equity        Payable Date    2018-09-21
        4  NVDA US Equity     Dividend Amount          0.15
        5  NVDA US Equity  Dividend Frequency       Quarter
        6  NVDA US Equity       Dividend Type  Regular Cash
        7  NVDA US Equity       Declared Date    2018-05-10
        >>> dvd = bds(
        ...     'NVDA US Equity', 'DVD_Hist_All',
        ...     DVD_Start_Dt=s_dt, DVD_End_Dt=e_dt,
        ... )
        >>> dvd.reset_index().loc[:, ['ticker', 'ex_date', 'dividend_amount']]
                   ticker     ex_date  dividend_amount
        0  NVDA US Equity  2018-08-29             0.15
        1  NVDA US Equity  2018-05-23             0.15
        >>> if not os.environ.get('BBG_ROOT', ''):
        ...     os.environ['BBG_ROOT'] = f'{files.abspath(__file__, 1)}/tests/data'
        >>> idx_kw = dict(End_Dt='20181220', cache=True)
        >>> idx_wt = bds('DJI Index', 'Indx_MWeight_Hist', **idx_kw)
        >>> idx_wt.round(2).tail().reset_index(drop=True)
          index_member  percent_weight
        0         V UN            3.82
        1        VZ UN            1.63
        2       WBA UW            2.06
        3       WMT UN            2.59
        4       XOM UN            2.04
        >>> idx_wt = bds('DJI Index', 'Indx_MWeight_Hist', **idx_kw)
        >>> idx_wt.round(2).head().reset_index(drop=True)
          index_member  percent_weight
        0      AAPL UW            4.65
        1       AXP UN            2.84
        2        BA UN            9.29
        3       CAT UN            3.61
        4      CSCO UW            1.26
    """
    logger = logs.get_logger(bds, level=kwargs.pop('log', logs.LOG_LEVEL))
    con, _ = create_connection()
    ovrds = assist.proc_ovrds(**kwargs)

    logger.info(
        f'loading block data from Bloomberg:\n'
        f'{assist.info_qry(tickers=tickers, flds=flds)}'
    )
    data = con.bulkref(tickers=tickers, flds=flds, ovrds=ovrds)
    if not kwargs.get('cache', False): return [data]

    qry_data = []
    for (ticker, fld), grp in data.groupby(['ticker', 'field']):
        data_file = storage.ref_file(
            ticker=ticker, fld=fld, ext='pkl',
            has_date=kwargs.get('has_date', True), **kwargs
        )
        if data_file:
            if not files.exists(data_file): qry_data.append(grp)
            files.create_folder(data_file, is_file=True)
            grp.reset_index(drop=True).to_pickle(data_file)

    return qry_data