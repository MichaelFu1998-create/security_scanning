def plot_sector_exposures_gross(gross_exposures, sector_dict=None, ax=None):
    """
    Plots output of compute_sector_exposures as area charts

    Parameters
    ----------
    gross_exposures : arrays
        Arrays of gross sector exposures (output of compute_sector_exposures).

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

    ax.stackplot(gross_exposures[0].index, gross_exposures,
                 labels=sector_names, colors=color_list, alpha=0.8,
                 baseline='zero')
    ax.axhline(0, color='k', linestyle='-')
    ax.set(title='Gross exposure to sectors',
           ylabel='Proportion of gross exposure \n in sectors')

    return ax