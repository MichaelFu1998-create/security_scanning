def format_earning(data: pd.DataFrame, header: pd.DataFrame) -> pd.DataFrame:
    """
    Standardized earning outputs and add percentage by each blocks

    Args:
        data: earning data block
        header: earning headers

    Returns:
        pd.DataFrame

    Examples:
        >>> format_earning(
        ...     data=pd.read_pickle('xbbg/tests/data/sample_earning.pkl'),
        ...     header=pd.read_pickle('xbbg/tests/data/sample_earning_header.pkl')
        ... ).round(2)
                         level  fy2017  fy2017_pct
        Asia-Pacific       1.0  3540.0       66.43
           China           2.0  1747.0       49.35
           Japan           2.0  1242.0       35.08
           Singapore       2.0   551.0       15.56
        United States      1.0  1364.0       25.60
        Europe             1.0   263.0        4.94
        Other Countries    1.0   162.0        3.04
    """
    if data.dropna(subset=['value']).empty: return pd.DataFrame()

    res = pd.concat([
        grp.loc[:, ['value']].set_index(header.value)
        for _, grp in data.groupby(data.position)
    ], axis=1)
    res.index.name = None
    res.columns = res.iloc[0]
    res = res.iloc[1:].transpose().reset_index().apply(
        pd.to_numeric, downcast='float', errors='ignore'
    )
    res.rename(
        columns=lambda vv: '_'.join(vv.lower().split()).replace('fy_', 'fy'),
        inplace=True,
    )

    years = res.columns[res.columns.str.startswith('fy')]
    lvl_1 = res.level == 1
    for yr in years:
        res.loc[:, yr] = res.loc[:, yr].round(1)
        pct = f'{yr}_pct'
        res.loc[:, pct] = 0.
        res.loc[lvl_1, pct] = res.loc[lvl_1, pct].astype(float).round(1)
        res.loc[lvl_1, pct] = res.loc[lvl_1, yr] / res.loc[lvl_1, yr].sum() * 100
        sub_pct = []
        for _, snap in res[::-1].iterrows():
            if snap.level > 2: continue
            if snap.level == 1:
                if len(sub_pct) == 0: continue
                sub = pd.concat(sub_pct, axis=1).transpose()
                res.loc[sub.index, pct] = \
                    res.loc[sub.index, yr] / res.loc[sub.index, yr].sum() * 100
                sub_pct = []
            if snap.level == 2: sub_pct.append(snap)

    res.set_index('segment_name', inplace=True)
    res.index.name = None
    return res