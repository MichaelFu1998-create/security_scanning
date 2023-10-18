def compute_volume_exposures(shares_held, volumes, percentile):
    """
    Returns arrays of pth percentile of long, short and gross volume exposures
    of an algorithm's held shares

    Parameters
    ----------
    shares_held : pd.DataFrame
        Daily number of shares held by an algorithm.
        - See full explanation in create_risk_tear_sheet

    volume : pd.DataFrame
        Daily volume per asset
        - See full explanation in create_risk_tear_sheet

    percentile : float
        Percentile to use when computing and plotting volume exposures
        - See full explanation in create_risk_tear_sheet
    """

    shares_held = shares_held.replace(0, np.nan)

    shares_longed = shares_held[shares_held > 0]
    shares_shorted = -1 * shares_held[shares_held < 0]
    shares_grossed = shares_held.abs()

    longed_frac = shares_longed.divide(volumes)
    shorted_frac = shares_shorted.divide(volumes)
    grossed_frac = shares_grossed.divide(volumes)

    # NOTE: To work around a bug in `quantile` with nan-handling in
    #       pandas 0.18, use np.nanpercentile by applying to each row of
    #       the dataframe. This is fixed in pandas 0.19.
    #
    # longed_threshold = 100*longed_frac.quantile(percentile, axis='columns')
    # shorted_threshold = 100*shorted_frac.quantile(percentile, axis='columns')
    # grossed_threshold = 100*grossed_frac.quantile(percentile, axis='columns')

    longed_threshold = 100 * longed_frac.apply(
        partial(np.nanpercentile, q=100 * percentile),
        axis='columns',
    )
    shorted_threshold = 100 * shorted_frac.apply(
        partial(np.nanpercentile, q=100 * percentile),
        axis='columns',
    )
    grossed_threshold = 100 * grossed_frac.apply(
        partial(np.nanpercentile, q=100 * percentile),
        axis='columns',
    )

    return longed_threshold, shorted_threshold, grossed_threshold