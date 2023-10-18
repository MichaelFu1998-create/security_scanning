def plot_rolling_volatility(returns, factor_returns=None,
                            rolling_window=APPROX_BDAYS_PER_MONTH * 6,
                            legend_loc='best', ax=None, **kwargs):
    """
    Plots the rolling volatility versus date.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.Series, optional
        Daily noncumulative returns of the benchmark factor to which betas are
        computed. Usually a benchmark such as market returns.
         - This is in the same style as returns.
    rolling_window : int, optional
        The days window over which to compute the volatility.
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

    y_axis_formatter = FuncFormatter(utils.two_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    rolling_vol_ts = timeseries.rolling_volatility(
        returns, rolling_window)
    rolling_vol_ts.plot(alpha=.7, lw=3, color='orangered', ax=ax,
                        **kwargs)
    if factor_returns is not None:
        rolling_vol_ts_factor = timeseries.rolling_volatility(
            factor_returns, rolling_window)
        rolling_vol_ts_factor.plot(alpha=.7, lw=3, color='grey', ax=ax,
                                   **kwargs)

    ax.set_title('Rolling volatility (6-month)')
    ax.axhline(
        rolling_vol_ts.mean(),
        color='steelblue',
        linestyle='--',
        lw=3)

    ax.axhline(0.0, color='black', linestyle='-', lw=2)

    ax.set_ylabel('Volatility')
    ax.set_xlabel('')
    if factor_returns is None:
        ax.legend(['Volatility', 'Average volatility'],
                  loc=legend_loc, frameon=True, framealpha=0.5)
    else:
        ax.legend(['Volatility', 'Benchmark volatility', 'Average volatility'],
                  loc=legend_loc, frameon=True, framealpha=0.5)
    return ax