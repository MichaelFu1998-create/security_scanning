def create_perf_attrib_tear_sheet(returns,
                                  positions,
                                  factor_returns,
                                  factor_loadings,
                                  transactions=None,
                                  pos_in_dollars=True,
                                  return_fig=False,
                                  factor_partitions=FACTOR_PARTITIONS):
    """
    Generate plots and tables for analyzing a strategy's performance.

    Parameters
    ----------
    returns : pd.Series
        Returns for each day in the date range.

    positions: pd.DataFrame
        Daily holdings (in dollars or percentages), indexed by date.
        Will be converted to percentages if positions are in dollars.
        Short positions show up as cash in the 'cash' column.

    factor_returns : pd.DataFrame
        Returns by factor, with date as index and factors as columns

    factor_loadings : pd.DataFrame
        Factor loadings for all days in the date range, with date
        and ticker as index, and factors as columns.

    transactions : pd.DataFrame, optional
        Prices and amounts of executed trades. One row per trade.
         - See full explanation in create_full_tear_sheet.
         - Default is None.

    pos_in_dollars : boolean, optional
        Flag indicating whether `positions` are in dollars or percentages
        If True, positions are in dollars.

    return_fig : boolean, optional
        If True, returns the figure that was plotted on.

    factor_partitions : dict
        dict specifying how factors should be separated in factor returns
        and risk exposures plots
        - Example:
          {'style': ['momentum', 'size', 'value', ...],
           'sector': ['technology', 'materials', ... ]}
    """
    portfolio_exposures, perf_attrib_data = perf_attrib.perf_attrib(
        returns, positions, factor_returns, factor_loadings, transactions,
        pos_in_dollars=pos_in_dollars
    )

    display(Markdown("## Performance Relative to Common Risk Factors"))

    # aggregate perf attrib stats and show summary table
    perf_attrib.show_perf_attrib_stats(returns, positions, factor_returns,
                                       factor_loadings, transactions,
                                       pos_in_dollars)

    # one section for the returns plot, and for each factor grouping
    # one section for factor returns, and one for risk exposures
    vertical_sections = 1 + 2 * max(len(factor_partitions), 1)
    current_section = 0

    fig = plt.figure(figsize=[14, vertical_sections * 6])

    gs = gridspec.GridSpec(vertical_sections, 1,
                           wspace=0.5, hspace=0.5)

    perf_attrib.plot_returns(perf_attrib_data,
                             ax=plt.subplot(gs[current_section]))
    current_section += 1

    if factor_partitions is not None:

        for factor_type, partitions in factor_partitions.iteritems():

            columns_to_select = perf_attrib_data.columns.intersection(
                partitions
            )

            perf_attrib.plot_factor_contribution_to_perf(
                perf_attrib_data[columns_to_select],
                ax=plt.subplot(gs[current_section]),
                title=(
                    'Cumulative common {} returns attribution'
                ).format(factor_type)
            )
            current_section += 1

        for factor_type, partitions in factor_partitions.iteritems():

            perf_attrib.plot_risk_exposures(
                portfolio_exposures[portfolio_exposures.columns
                                    .intersection(partitions)],
                ax=plt.subplot(gs[current_section]),
                title='Daily {} factor exposures'.format(factor_type)
            )
            current_section += 1

    else:

        perf_attrib.plot_factor_contribution_to_perf(
            perf_attrib_data,
            ax=plt.subplot(gs[current_section])
        )
        current_section += 1

        perf_attrib.plot_risk_exposures(
            portfolio_exposures,
            ax=plt.subplot(gs[current_section])
        )

    gs.tight_layout(fig)

    if return_fig:
        return fig