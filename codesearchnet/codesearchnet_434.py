def plot_long_short_holdings(returns, positions,
                             legend_loc='upper left', ax=None, **kwargs):
    """
    Plots total amount of stocks with an active position, breaking out
    short and long into transparent filled regions.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    positions : pd.DataFrame, optional
        Daily net position values.
         - See full explanation in tears.create_full_tear_sheet.
    legend_loc : matplotlib.loc, optional
        The location of the legend on the plot.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.

    """

    if ax is None:
        ax = plt.gca()

    positions = positions.drop('cash', axis='columns')
    positions = positions.replace(0, np.nan)
    df_longs = positions[positions > 0].count(axis=1)
    df_shorts = positions[positions < 0].count(axis=1)
    lf = ax.fill_between(df_longs.index, 0, df_longs.values,
                         color='g', alpha=0.5, lw=2.0)
    sf = ax.fill_between(df_shorts.index, 0, df_shorts.values,
                         color='r', alpha=0.5, lw=2.0)

    bf = patches.Rectangle([0, 0], 1, 1, color='darkgoldenrod')
    leg = ax.legend([lf, sf, bf],
                    ['Long (max: %s, min: %s)' % (df_longs.max(),
                                                  df_longs.min()),
                     'Short (max: %s, min: %s)' % (df_shorts.max(),
                                                   df_shorts.min()),
                     'Overlap'], loc=legend_loc, frameon=True,
                    framealpha=0.5)
    leg.get_frame().set_edgecolor('black')

    ax.set_xlim((returns.index[0], returns.index[-1]))
    ax.set_title('Long and short holdings')
    ax.set_ylabel('Holdings')
    ax.set_xlabel('')
    return ax