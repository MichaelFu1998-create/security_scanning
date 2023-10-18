def show_and_plot_top_positions(returns, positions_alloc,
                                show_and_plot=2, hide_positions=False,
                                legend_loc='real_best', ax=None,
                                **kwargs):
    """
    Prints and/or plots the exposures of the top 10 held positions of
    all time.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    positions_alloc : pd.DataFrame
        Portfolio allocation of positions. See pos.get_percent_alloc.
    show_and_plot : int, optional
        By default, this is 2, and both prints and plots.
        If this is 0, it will only plot; if 1, it will only print.
    hide_positions : bool, optional
        If True, will not output any symbol names.
    legend_loc : matplotlib.loc, optional
        The location of the legend on the plot.
        By default, the legend will display below the plot.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.

    Returns
    -------
    ax : matplotlib.Axes, conditional
        The axes that were plotted on.

    """
    positions_alloc = positions_alloc.copy()
    positions_alloc.columns = positions_alloc.columns.map(utils.format_asset)

    df_top_long, df_top_short, df_top_abs = pos.get_top_long_short_abs(
        positions_alloc)

    if show_and_plot == 1 or show_and_plot == 2:
        utils.print_table(pd.DataFrame(df_top_long * 100, columns=['max']),
                          float_format='{0:.2f}%'.format,
                          name='Top 10 long positions of all time')

        utils.print_table(pd.DataFrame(df_top_short * 100, columns=['max']),
                          float_format='{0:.2f}%'.format,
                          name='Top 10 short positions of all time')

        utils.print_table(pd.DataFrame(df_top_abs * 100, columns=['max']),
                          float_format='{0:.2f}%'.format,
                          name='Top 10 positions of all time')

    if show_and_plot == 0 or show_and_plot == 2:

        if ax is None:
            ax = plt.gca()

        positions_alloc[df_top_abs.index].plot(
            title='Portfolio allocation over time, only top 10 holdings',
            alpha=0.5, ax=ax, **kwargs)

        # Place legend below plot, shrink plot by 20%
        if legend_loc == 'real_best':
            box = ax.get_position()
            ax.set_position([box.x0, box.y0 + box.height * 0.1,
                             box.width, box.height * 0.9])

            # Put a legend below current axis
            ax.legend(loc='upper center', frameon=True, framealpha=0.5,
                      bbox_to_anchor=(0.5, -0.14), ncol=5)
        else:
            ax.legend(loc=legend_loc)

        ax.set_xlim((returns.index[0], returns.index[-1]))
        ax.set_ylabel('Exposure by holding')

        if hide_positions:
            ax.legend_.remove()

        return ax