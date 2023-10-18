def plot_volume_exposures_longshort(longed_threshold, shorted_threshold,
                                    percentile, ax=None):
    """
    Plots outputs of compute_volume_exposures as line graphs

    Parameters
    ----------
    longed_threshold, shorted_threshold : pd.Series
        Series of longed and shorted volume exposures (output of
        compute_volume_exposures).

    percentile : float
        Percentile to use when computing and plotting volume exposures.
        - See full explanation in create_risk_tear_sheet
    """

    if ax is None:
        ax = plt.gca()

    ax.plot(longed_threshold.index, longed_threshold,
            color='b', label='long')
    ax.plot(shorted_threshold.index, shorted_threshold,
            color='r', label='short')
    ax.axhline(0, color='k')
    ax.set(title='Long and short exposures to illiquidity',
           ylabel='{}th percentile of proportion of volume (%)'
           .format(100 * percentile))
    ax.legend(frameon=True, framealpha=0.5)

    return ax