def plot_risk_exposures(exposures, ax=None,
                        title='Daily risk factor exposures'):
    """
    Parameters
    ----------
    exposures : pd.DataFrame
        df indexed by datetime, with factors as columns
        - Example:
                        momentum  reversal
            dt
            2017-01-01 -0.238655  0.077123
            2017-01-02  0.821872  1.520515

    ax :  matplotlib.axes.Axes
        axes on which plots are made. if None, current axes will be used

    Returns
    -------
    ax :  matplotlib.axes.Axes
    """
    if ax is None:
        ax = plt.gca()

    for col in exposures:
        ax.plot(exposures[col])

    configure_legend(ax, change_colors=True)
    ax.set_ylabel('Factor exposures')
    ax.set_title(title)

    return ax