def compute_style_factor_exposures(positions, risk_factor):
    """
    Returns style factor exposure of an algorithm's positions

    Parameters
    ----------
    positions : pd.DataFrame
        Daily equity positions of algorithm, in dollars.
        - See full explanation in create_risk_tear_sheet

    risk_factor : pd.DataFrame
        Daily risk factor per asset.
        - DataFrame with dates as index and equities as columns
        - Example:
                         Equity(24   Equity(62
                           [AAPL])      [ABT])
        2017-04-03	  -0.51284     1.39173
        2017-04-04	  -0.73381     0.98149
        2017-04-05	  -0.90132     1.13981
    """

    positions_wo_cash = positions.drop('cash', axis='columns')
    gross_exposure = positions_wo_cash.abs().sum(axis='columns')

    style_factor_exposure = positions_wo_cash.multiply(risk_factor) \
        .divide(gross_exposure, axis='index')
    tot_style_factor_exposure = style_factor_exposure.sum(axis='columns',
                                                          skipna=True)

    return tot_style_factor_exposure