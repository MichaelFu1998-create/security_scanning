def plot_volume_exposures_gross(grossed_threshold, percentile, ax=None):
    """
    Plots outputs of compute_volume_exposures as line graphs

    Parameters
    ----------
    grossed_threshold : pd.Series
        Series of grossed volume exposures (output of
        compute_volume_exposures).

    percentile : float
        Percentile to use when computing and plotting volume exposures
        - See full explanation in create_risk_tear_sheet
    """

    if ax is None:
        ax = plt.gca()

    ax.plot(grossed_threshold.index, grossed_threshold,
            color='b', label='gross')
    ax.axhline(0, color='k')
    ax.set(title='Gross exposure to illiquidity',
           ylabel='{}th percentile of \n proportion of volume (%)'
           .format(100 * percentile))
    ax.legend(frameon=True, framealpha=0.5)

    return ax