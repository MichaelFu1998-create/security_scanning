def plot_style_factor_exposures(tot_style_factor_exposure, factor_name=None,
                                ax=None):
    """
    Plots DataFrame output of compute_style_factor_exposures as a line graph

    Parameters
    ----------
    tot_style_factor_exposure : pd.Series
        Daily style factor exposures (output of compute_style_factor_exposures)
        - Time series with decimal style factor exposures
        - Example:
            2017-04-24    0.037820
            2017-04-25    0.016413
            2017-04-26   -0.021472
            2017-04-27   -0.024859

    factor_name : string
        Name of style factor, for use in graph title
        - Defaults to tot_style_factor_exposure.name
    """

    if ax is None:
        ax = plt.gca()

    if factor_name is None:
        factor_name = tot_style_factor_exposure.name

    ax.plot(tot_style_factor_exposure.index, tot_style_factor_exposure,
            label=factor_name)
    avg = tot_style_factor_exposure.mean()
    ax.axhline(avg, linestyle='-.', label='Mean = {:.3}'.format(avg))
    ax.axhline(0, color='k', linestyle='-')
    _, _, y1, y2 = plt.axis()
    lim = max(abs(y1), abs(y2))
    ax.set(title='Exposure to {}'.format(factor_name),
           ylabel='{} \n weighted exposure'.format(factor_name),
           ylim=(-lim, lim))
    ax.legend(frameon=True, framealpha=0.5)

    return ax