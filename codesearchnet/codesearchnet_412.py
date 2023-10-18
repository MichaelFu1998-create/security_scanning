def _align_and_warn(returns,
                    positions,
                    factor_returns,
                    factor_loadings,
                    transactions=None,
                    pos_in_dollars=True):
    """
    Make sure that all inputs have matching dates and tickers,
    and raise warnings if necessary.
    """
    missing_stocks = positions.columns.difference(
        factor_loadings.index.get_level_values(1).unique()
    )

    # cash will not be in factor_loadings
    num_stocks = len(positions.columns) - 1
    missing_stocks = missing_stocks.drop('cash')
    num_stocks_covered = num_stocks - len(missing_stocks)
    missing_ratio = round(len(missing_stocks) / num_stocks, ndigits=3)

    if num_stocks_covered == 0:
        raise ValueError("Could not perform performance attribution. "
                         "No factor loadings were available for this "
                         "algorithm's positions.")

    if len(missing_stocks) > 0:

        if len(missing_stocks) > 5:

            missing_stocks_displayed = (
                " {} assets were missing factor loadings, including: {}..{}"
            ).format(len(missing_stocks),
                     ', '.join(missing_stocks[:5].map(str)),
                     missing_stocks[-1])
            avg_allocation_msg = "selected missing assets"

        else:
            missing_stocks_displayed = (
                "The following assets were missing factor loadings: {}."
            ).format(list(missing_stocks))
            avg_allocation_msg = "missing assets"

        missing_stocks_warning_msg = (
            "Could not determine risk exposures for some of this algorithm's "
            "positions. Returns from the missing assets will not be properly "
            "accounted for in performance attribution.\n"
            "\n"
            "{}. "
            "Ignoring for exposure calculation and performance attribution. "
            "Ratio of assets missing: {}. Average allocation of {}:\n"
            "\n"
            "{}.\n"
        ).format(
            missing_stocks_displayed,
            missing_ratio,
            avg_allocation_msg,
            positions[missing_stocks[:5].union(missing_stocks[[-1]])].mean(),
        )

        warnings.warn(missing_stocks_warning_msg)

        positions = positions.drop(missing_stocks, axis='columns',
                                   errors='ignore')

    missing_factor_loadings_index = positions.index.difference(
        factor_loadings.index.get_level_values(0).unique()
    )

    missing_factor_loadings_index = positions.index.difference(
        factor_loadings.index.get_level_values(0).unique()
    )

    if len(missing_factor_loadings_index) > 0:

        if len(missing_factor_loadings_index) > 5:
            missing_dates_displayed = (
                "(first missing is {}, last missing is {})"
            ).format(
                missing_factor_loadings_index[0],
                missing_factor_loadings_index[-1]
            )
        else:
            missing_dates_displayed = list(missing_factor_loadings_index)

        warning_msg = (
            "Could not find factor loadings for {} dates: {}. "
            "Truncating date range for performance attribution. "
        ).format(len(missing_factor_loadings_index), missing_dates_displayed)

        warnings.warn(warning_msg)

        positions = positions.drop(missing_factor_loadings_index,
                                   errors='ignore')
        returns = returns.drop(missing_factor_loadings_index, errors='ignore')
        factor_returns = factor_returns.drop(missing_factor_loadings_index,
                                             errors='ignore')

    if transactions is not None and pos_in_dollars:
        turnover = get_turnover(positions, transactions).mean()
        if turnover > PERF_ATTRIB_TURNOVER_THRESHOLD:
            warning_msg = (
                "This algorithm has relatively high turnover of its "
                "positions. As a result, performance attribution might not be "
                "fully accurate.\n"
                "\n"
                "Performance attribution is calculated based "
                "on end-of-day holdings and does not account for intraday "
                "activity. Algorithms that derive a high percentage of "
                "returns from buying and selling within the same day may "
                "receive inaccurate performance attribution.\n"
            )
            warnings.warn(warning_msg)

    return (returns, positions, factor_returns, factor_loadings)