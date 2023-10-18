def format_intraday(data: pd.DataFrame, ticker, **kwargs) -> pd.DataFrame:
    """
    Format intraday data

    Args:
        data: pd.DataFrame from bdib
        ticker: ticker

    Returns:
        pd.DataFrame

    Examples:
        >>> format_intraday(
        ...     data=pd.read_parquet('xbbg/tests/data/sample_bdib.parq'),
        ...     ticker='SPY US Equity',
        ... ).xs('close', axis=1, level=1, drop_level=False)
        ticker                    SPY US Equity
        field                             close
        2018-12-28 09:30:00-05:00        249.67
        2018-12-28 09:31:00-05:00        249.54
        2018-12-28 09:32:00-05:00        249.22
        2018-12-28 09:33:00-05:00        249.01
        2018-12-28 09:34:00-05:00        248.86
        >>> format_intraday(
        ...     data=pd.read_parquet('xbbg/tests/data/sample_bdib.parq'),
        ...     ticker='SPY US Equity', price_only=True
        ... )
        ticker                     SPY US Equity
        2018-12-28 09:30:00-05:00         249.67
        2018-12-28 09:31:00-05:00         249.54
        2018-12-28 09:32:00-05:00         249.22
        2018-12-28 09:33:00-05:00         249.01
        2018-12-28 09:34:00-05:00         248.86
    """
    if data.empty: return pd.DataFrame()
    data.columns = pd.MultiIndex.from_product([
        [ticker], data.rename(columns=dict(numEvents='num_trds')).columns
    ], names=['ticker', 'field'])
    data.index.name = None
    if kwargs.get('price_only', False):
        kw_xs = dict(axis=1, level=1)
        close = data.xs('close', **kw_xs)
        volume = data.xs('volume', **kw_xs).iloc[:, 0]
        return close.loc[volume > 0] if volume.min() > 0 else close
    else: return data