def show_perf_attrib_stats(returns,
                           positions,
                           factor_returns,
                           factor_loadings,
                           transactions=None,
                           pos_in_dollars=True):
    """
    Calls `perf_attrib` using inputs, and displays outputs using
    `utils.print_table`.
    """
    risk_exposures, perf_attrib_data = perf_attrib(
        returns,
        positions,
        factor_returns,
        factor_loadings,
        transactions,
        pos_in_dollars=pos_in_dollars,
    )

    perf_attrib_stats, risk_exposure_stats =\
        create_perf_attrib_stats(perf_attrib_data, risk_exposures)

    percentage_formatter = '{:.2%}'.format
    float_formatter = '{:.2f}'.format

    summary_stats = perf_attrib_stats.loc[['Annualized Specific Return',
                                           'Annualized Common Return',
                                           'Annualized Total Return',
                                           'Specific Sharpe Ratio']]

    # Format return rows in summary stats table as percentages.
    for col_name in (
        'Annualized Specific Return',
        'Annualized Common Return',
        'Annualized Total Return',
    ):
        summary_stats[col_name] = percentage_formatter(summary_stats[col_name])

    # Display sharpe to two decimal places.
    summary_stats['Specific Sharpe Ratio'] = float_formatter(
        summary_stats['Specific Sharpe Ratio']
    )

    print_table(summary_stats, name='Summary Statistics')

    print_table(
        risk_exposure_stats,
        name='Exposures Summary',
        # In exposures table, format exposure column to 2 decimal places, and
        # return columns  as percentages.
        formatters={
            'Average Risk Factor Exposure': float_formatter,
            'Annualized Return': percentage_formatter,
            'Cumulative Return': percentage_formatter,
        },
    )