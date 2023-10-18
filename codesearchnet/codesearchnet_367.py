def plot_sector_exposures_longshort(long_exposures, short_exposures,
                                    sector_dict=SECTORS, ax=None):
    """
    Plots outputs of compute_sector_exposures as area charts

    Parameters
    ----------
    long_exposures, short_exposures : arrays
        Arrays of long and short sector exposures (output of
        compute_sector_exposures).

    sector_dict : dict or OrderedDict
        Dictionary of all sectors
        - See full description in compute_sector_exposures
    """

    if ax is None:
        ax = plt.gca()

    if sector_dict is None:
        sector_names = SECTORS.values()
    else:
        sector_names = sector_dict.values()

    color_list = plt.cm.gist_rainbow(np.linspace(0, 1, 11))

    ax.stackplot(long_exposures[0].index, long_exposures,
                 labels=sector_names, colors=color_list, alpha=0.8,
                 baseline='zero')
    ax.stackplot(long_exposures[0].index, short_exposures,
                 colors=color_list, alpha=0.8, baseline='zero')
    ax.axhline(0, color='k', linestyle='-')
    ax.set(title='Long and short exposures to sectors',
           ylabel='Proportion of long/short exposure in sectors')
    ax.legend(loc='upper left', frameon=True, framealpha=0.5)

    return ax