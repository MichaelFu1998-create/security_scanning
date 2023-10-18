def compute_cap_exposures(positions, caps):
    """
    Returns arrays of long, short and gross market cap exposures of an
    algorithm's positions

    Parameters
    ----------
    positions : pd.DataFrame
        Daily equity positions of algorithm, in dollars.
        - See full explanation in compute_style_factor_exposures.

    caps : pd.DataFrame
        Daily Morningstar sector code per asset
        - See full explanation in create_risk_tear_sheet
    """

    long_exposures = []
    short_exposures = []
    gross_exposures = []
    net_exposures = []

    positions_wo_cash = positions.drop('cash', axis='columns')
    tot_gross_exposure = positions_wo_cash.abs().sum(axis='columns')
    tot_long_exposure = positions_wo_cash[positions_wo_cash > 0] \
        .sum(axis='columns')
    tot_short_exposure = positions_wo_cash[positions_wo_cash < 0] \
        .abs().sum(axis='columns')

    for bucket_name, boundaries in CAP_BUCKETS.items():
        in_bucket = positions_wo_cash[(caps >= boundaries[0]) &
                                      (caps <= boundaries[1])]

        gross_bucket = in_bucket.abs().sum(axis='columns') \
            .divide(tot_gross_exposure)
        long_bucket = in_bucket[in_bucket > 0] \
            .sum(axis='columns').divide(tot_long_exposure)
        short_bucket = in_bucket[in_bucket < 0] \
            .sum(axis='columns').divide(tot_short_exposure)
        net_bucket = long_bucket.subtract(short_bucket)

        gross_exposures.append(gross_bucket)
        long_exposures.append(long_bucket)
        short_exposures.append(short_bucket)
        net_exposures.append(net_bucket)

    return long_exposures, short_exposures, gross_exposures, net_exposures