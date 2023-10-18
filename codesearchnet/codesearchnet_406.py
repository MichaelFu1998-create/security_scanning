def create_perf_attrib_stats(perf_attrib, risk_exposures):
    """
    Takes perf attribution data over a period of time and computes annualized
    multifactor alpha, multifactor sharpe, risk exposures.
    """
    summary = OrderedDict()
    total_returns = perf_attrib['total_returns']
    specific_returns = perf_attrib['specific_returns']
    common_returns = perf_attrib['common_returns']

    summary['Annualized Specific Return'] =\
        ep.annual_return(specific_returns)
    summary['Annualized Common Return'] =\
        ep.annual_return(common_returns)
    summary['Annualized Total Return'] =\
        ep.annual_return(total_returns)

    summary['Specific Sharpe Ratio'] =\
        ep.sharpe_ratio(specific_returns)

    summary['Cumulative Specific Return'] =\
        ep.cum_returns_final(specific_returns)
    summary['Cumulative Common Return'] =\
        ep.cum_returns_final(common_returns)
    summary['Total Returns'] =\
        ep.cum_returns_final(total_returns)

    summary = pd.Series(summary, name='')

    annualized_returns_by_factor = [ep.annual_return(perf_attrib[c])
                                    for c in risk_exposures.columns]
    cumulative_returns_by_factor = [ep.cum_returns_final(perf_attrib[c])
                                    for c in risk_exposures.columns]

    risk_exposure_summary = pd.DataFrame(
        data=OrderedDict([
            (
                'Average Risk Factor Exposure',
                risk_exposures.mean(axis='rows')
            ),
            ('Annualized Return', annualized_returns_by_factor),
            ('Cumulative Return', cumulative_returns_by_factor),
        ]),
        index=risk_exposures.columns,
    )

    return summary, risk_exposure_summary