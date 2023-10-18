def plot_gross_leverage(returns, positions, ax=None, **kwargs):
    """
    Plots gross leverage versus date.

    Gross leverage is the sum of long and short exposure per share
    divided by net asset value.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    positions : pd.DataFrame
        Daily net position values.
         - See full explanation in create_full_tear_sheet.
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
    gl = timeseries.gross_lev(positions)
    gl.plot(lw=0.5, color='limegreen', legend=False, ax=ax, **kwargs)

    ax.axhline(gl.mean(), color='g', linestyle='--', lw=3)

    ax.set_title('Gross leverage')
    ax.set_ylabel('Gross leverage')
    ax.set_xlabel('')
    return ax