def earning(
        ticker, by='Geo', typ='Revenue', ccy=None, level=None, **kwargs
) -> pd.DataFrame:
    """
    Earning exposures by Geo or Products

    Args:
        ticker: ticker name
        by: [G(eo), P(roduct)]
        typ: type of earning, start with `PG_` in Bloomberg FLDS - default `Revenue`
        ccy: currency of earnings
        level: hierarchy level of earnings

    Returns:
        pd.DataFrame

    Examples:
        >>> data = earning('AMD US Equity', Eqy_Fund_Year=2017, Number_Of_Periods=1)
        >>> data.round(2)
                         level  fy2017  fy2017_pct
        Asia-Pacific       1.0  3540.0       66.43
           China           2.0  1747.0       49.35
           Japan           2.0  1242.0       35.08
           Singapore       2.0   551.0       15.56
        United States      1.0  1364.0       25.60
        Europe             1.0   263.0        4.94
        Other Countries    1.0   162.0        3.04
    """
    ovrd = 'G' if by[0].upper() == 'G' else 'P'
    new_kw = dict(raw=True, Product_Geo_Override=ovrd)
    header = bds(tickers=ticker, flds='PG_Bulk_Header', **new_kw, **kwargs)
    if ccy: kwargs['Eqy_Fund_Crncy'] = ccy
    if level: kwargs['PG_Hierarchy_Level'] = level
    data = bds(tickers=ticker, flds=f'PG_{typ}', **new_kw, **kwargs)
    return assist.format_earning(data=data, header=header)