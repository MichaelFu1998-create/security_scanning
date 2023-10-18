def show_profit_attribution(round_trips):
    """
    Prints the share of total PnL contributed by each
    traded name.

    Parameters
    ----------
    round_trips : pd.DataFrame
        DataFrame with one row per round trip trade.
        - See full explanation in round_trips.extract_round_trips
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    total_pnl = round_trips['pnl'].sum()
    pnl_attribution = round_trips.groupby('symbol')['pnl'].sum() / total_pnl
    pnl_attribution.name = ''

    pnl_attribution.index = pnl_attribution.index.map(utils.format_asset)
    utils.print_table(
        pnl_attribution.sort_values(
            inplace=False,
            ascending=False,
        ),
        name='Profitability (PnL / PnL total) per name',
        float_format='{:.2%}'.format,
    )