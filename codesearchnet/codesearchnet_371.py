def plot_cap_exposures_longshort(long_exposures, short_exposures, ax=None):
    """
    Plots outputs of compute_cap_exposures as area charts

    Parameters
    ----------
    long_exposures, short_exposures : arrays
        Arrays of long and short market cap exposures (output of
        compute_cap_exposures).
    """

    if ax is None:
        ax = plt.gca()

    color_list = plt.cm.gist_rainbow(np.linspace(0, 1, 5))

    ax.stackplot(long_exposures[0].index, long_exposures,
                 labels=CAP_BUCKETS.keys(), colors=color_list, alpha=0.8,
                 baseline='zero')
    ax.stackplot(long_exposures[0].index, short_exposures, colors=color_list,
                 alpha=0.8, baseline='zero')
    ax.axhline(0, color='k', linestyle='-')
    ax.set(title='Long and short exposures to market caps',
           ylabel='Proportion of long/short exposure in market cap buckets')
    ax.legend(loc='upper left', frameon=True, framealpha=0.5)

    return ax