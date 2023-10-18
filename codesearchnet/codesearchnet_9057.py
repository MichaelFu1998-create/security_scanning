def dividend(
        tickers, typ='all', start_date=None, end_date=None, **kwargs
) -> pd.DataFrame:
    """
    Bloomberg dividend / split history

    Args:
        tickers: list of tickers
        typ: dividend adjustment type
            `all`:       `DVD_Hist_All`
            `dvd`:       `DVD_Hist`
            `split`:     `Eqy_DVD_Hist_Splits`
            `gross`:     `Eqy_DVD_Hist_Gross`
            `adjust`:    `Eqy_DVD_Adjust_Fact`
            `adj_fund`:  `Eqy_DVD_Adj_Fund`
            `with_amt`:  `DVD_Hist_All_with_Amt_Status`
            `dvd_amt`:   `DVD_Hist_with_Amt_Status`
            `gross_amt`: `DVD_Hist_Gross_with_Amt_Stat`
            `projected`: `BDVD_Pr_Ex_Dts_DVD_Amts_w_Ann`
        start_date: start date
        end_date: end date
        **kwargs: overrides

    Returns:
        pd.DataFrame

    Examples:
        >>> res = dividend(
        ...     tickers=['C US Equity', 'NVDA US Equity', 'MS US Equity'],
        ...     start_date='2018-01-01', end_date='2018-05-01'
        ... )
        >>> res.index.name = None
        >>> res.loc[:, ['ex_date', 'rec_date', 'dvd_amt']].round(2)
                           ex_date    rec_date  dvd_amt
        C US Equity     2018-02-02  2018-02-05     0.32
        MS US Equity    2018-04-27  2018-04-30     0.25
        MS US Equity    2018-01-30  2018-01-31     0.25
        NVDA US Equity  2018-02-22  2018-02-23     0.15
    """
    if isinstance(tickers, str): tickers = [tickers]
    tickers = [t for t in tickers if ('Equity' in t) and ('=' not in t)]

    fld = {
        'all': 'DVD_Hist_All', 'dvd': 'DVD_Hist',
        'split': 'Eqy_DVD_Hist_Splits', 'gross': 'Eqy_DVD_Hist_Gross',
        'adjust': 'Eqy_DVD_Adjust_Fact', 'adj_fund': 'Eqy_DVD_Adj_Fund',
        'with_amt': 'DVD_Hist_All_with_Amt_Status',
        'dvd_amt': 'DVD_Hist_with_Amt_Status',
        'gross_amt': 'DVD_Hist_Gross_with_Amt_Stat',
        'projected': 'BDVD_Pr_Ex_Dts_DVD_Amts_w_Ann',
    }.get(typ, typ)

    if (fld == 'Eqy_DVD_Adjust_Fact') and ('Corporate_Actions_Filter' not in kwargs):
        kwargs['Corporate_Actions_Filter'] = 'NORMAL_CASH|ABNORMAL_CASH|CAPITAL_CHANGE'

    if fld in [
        'DVD_Hist_All', 'DVD_Hist', 'Eqy_DVD_Hist_Gross',
        'DVD_Hist_All_with_Amt_Status', 'DVD_Hist_with_Amt_Status',
    ]:
        if start_date: kwargs['DVD_Start_Dt'] = utils.fmt_dt(start_date, fmt='%Y%m%d')
        if end_date: kwargs['DVD_End_Dt'] = utils.fmt_dt(end_date, fmt='%Y%m%d')

    kwargs['col_maps'] = {
        'Declared Date': 'dec_date', 'Ex-Date': 'ex_date',
        'Record Date': 'rec_date', 'Payable Date': 'pay_date',
        'Dividend Amount': 'dvd_amt', 'Dividend Frequency': 'dvd_freq',
        'Dividend Type': 'dvd_type', 'Amount Status': 'amt_status',
        'Adjustment Date': 'adj_date', 'Adjustment Factor': 'adj_factor',
        'Adjustment Factor Operator Type': 'adj_op',
        'Adjustment Factor Flag': 'adj_flag',
        'Amount Per Share': 'amt_ps', 'Projected/Confirmed': 'category',
    }

    return bds(tickers=tickers, flds=fld, raw=False, **kwargs)