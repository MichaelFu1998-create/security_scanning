def plot_cap_exposures_gross(gross_exposures, ax=None):
    """
    Plots outputs of compute_cap_exposures as area charts

    Parameters
    ----------
    gross_exposures : array
        Arrays of gross market cap exposures (output of compute_cap_exposures).
    """

    if ax is None:
        ax = plt.gca()

    color_list = plt.cm.gist_rainbow(np.linspace(0, 1, 5))

    ax.stackplot(gross_exposures[0].index, gross_exposures,
                 labels=CAP_BUCKETS.keys(), colors=color_list, alpha=0.8,
                 baseline='zero')
    ax.axhline(0, color='k', linestyle='-')
    ax.set(title='Gross exposure to market caps',
           ylabel='Proportion of gross exposure \n in market cap buckets')

    return ax