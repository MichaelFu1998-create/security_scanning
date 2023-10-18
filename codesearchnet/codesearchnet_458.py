def plot_round_trip_lifetimes(round_trips, disp_amount=16, lsize=18, ax=None):
    """
    Plots timespans and directions of a sample of round trip trades.

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

    if ax is None:
        ax = plt.subplot()

    symbols_sample = round_trips.symbol.unique()
    np.random.seed(1)
    sample = np.random.choice(round_trips.symbol.unique(), replace=False,
                              size=min(disp_amount, len(symbols_sample)))
    sample_round_trips = round_trips[round_trips.symbol.isin(sample)]

    symbol_idx = pd.Series(np.arange(len(sample)), index=sample)

    for symbol, sym_round_trips in sample_round_trips.groupby('symbol'):
        for _, row in sym_round_trips.iterrows():
            c = 'b' if row.long else 'r'
            y_ix = symbol_idx[symbol] + 0.05
            ax.plot([row['open_dt'], row['close_dt']],
                    [y_ix, y_ix], color=c,
                    linewidth=lsize, solid_capstyle='butt')

    ax.set_yticks(range(disp_amount))
    ax.set_yticklabels([utils.format_asset(s) for s in sample])

    ax.set_ylim((-0.5, min(len(sample), disp_amount) - 0.5))
    blue = patches.Rectangle([0, 0], 1, 1, color='b', label='Long')
    red = patches.Rectangle([0, 0], 1, 1, color='r', label='Short')
    leg = ax.legend(handles=[blue, red], loc='lower left',
                    frameon=True, framealpha=0.5)
    leg.get_frame().set_edgecolor('black')
    ax.grid(False)

    return ax