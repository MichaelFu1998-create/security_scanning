def format_output(data: pd.DataFrame, source, col_maps=None) -> pd.DataFrame:
    """
    Format `pdblp` outputs to column-based results

    Args:
        data: `pdblp` result
        source: `bdp` or `bds`
        col_maps: rename columns with these mappings

    Returns:
        pd.DataFrame

    Examples:
        >>> format_output(
        ...     data=pd.read_pickle('xbbg/tests/data/sample_bdp.pkl'),
        ...     source='bdp'
        ... ).reset_index()
                  ticker                        name
        0  QQQ US Equity  INVESCO QQQ TRUST SERIES 1
        1  SPY US Equity      SPDR S&P 500 ETF TRUST
        >>> format_output(
        ...     data=pd.read_pickle('xbbg/tests/data/sample_dvd.pkl'),
        ...     source='bds', col_maps={'Dividend Frequency': 'dvd_freq'}
        ... ).loc[:, ['ex_date', 'dividend_amount', 'dvd_freq']].reset_index()
                ticker     ex_date  dividend_amount dvd_freq
        0  C US Equity  2018-02-02             0.32  Quarter
    """
    if data.empty: return pd.DataFrame()
    if source == 'bdp': req_cols = ['ticker', 'field', 'value']
    else: req_cols = ['ticker', 'field', 'name', 'value', 'position']
    if any(col not in data for col in req_cols): return pd.DataFrame()
    if data.dropna(subset=['value']).empty: return pd.DataFrame()

    if source == 'bdp':
        res = pd.DataFrame(pd.concat([
            pd.Series({**{'ticker': t}, **grp.set_index('field').value.to_dict()})
            for t, grp in data.groupby('ticker')
        ], axis=1, sort=False)).transpose().set_index('ticker')
    else:
        res = pd.DataFrame(pd.concat([
            grp.loc[:, ['name', 'value']].set_index('name')
            .transpose().reset_index(drop=True).assign(ticker=t)
            for (t, _), grp in data.groupby(['ticker', 'position'])
        ], sort=False)).reset_index(drop=True).set_index('ticker')
        res.columns.name = None

    if col_maps is None: col_maps = dict()
    return res.rename(
        columns=lambda vv: col_maps.get(
            vv, vv.lower().replace(' ', '_').replace('-', '_')
        )
    ).apply(pd.to_numeric, errors='ignore', downcast='float')