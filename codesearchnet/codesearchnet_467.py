def rolling_regression(returns, factor_returns,
                       rolling_window=APPROX_BDAYS_PER_MONTH * 6,
                       nan_threshold=0.1):
    """
    Computes rolling factor betas using a multivariate linear regression
    (separate linear regressions is problematic because the factors may be
    confounded).

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.DataFrame
        Daily noncumulative returns of the benchmark factor to which betas are
        computed. Usually a benchmark such as market returns.
         - Computes rolling beta for each column.
         - This is in the same style as returns.
    rolling_window : int, optional
        The days window over which to compute the beta. Defaults to 6 months.
    nan_threshold : float, optional
        If there are more than this fraction of NaNs, the rolling regression
        for the given date will be skipped.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing rolling beta coefficients to SMB, HML and UMD
    """

    # We need to drop NaNs to regress
    ret_no_na = returns.dropna()

    columns = ['alpha'] + factor_returns.columns.tolist()
    rolling_risk = pd.DataFrame(columns=columns,
                                index=ret_no_na.index)

    rolling_risk.index.name = 'dt'

    for beg, end in zip(ret_no_na.index[:-rolling_window],
                        ret_no_na.index[rolling_window:]):
        returns_period = ret_no_na[beg:end]
        factor_returns_period = factor_returns.loc[returns_period.index]

        if np.all(factor_returns_period.isnull().mean()) < nan_threshold:
            factor_returns_period_dnan = factor_returns_period.dropna()
            reg = linear_model.LinearRegression(fit_intercept=True).fit(
                factor_returns_period_dnan,
                returns_period.loc[factor_returns_period_dnan.index])
            rolling_risk.loc[end, factor_returns.columns] = reg.coef_
            rolling_risk.loc[end, 'alpha'] = reg.intercept_

    return rolling_risk