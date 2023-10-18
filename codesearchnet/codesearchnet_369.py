def plot_sector_exposures_net(net_exposures, sector_dict=None, ax=None):
    """
    Plots output of compute_sector_exposures as line graphs

    Parameters
    ----------
    net_exposures : arrays
        Arrays of net sector exposures (output of compute_sector_exposures).

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

    for i in range(len(net_exposures)):
        ax.plot(net_exposures[i], color=color_list[i], alpha=0.8,
                label=sector_names[i])
    ax.set(title='Net exposures to sectors',
           ylabel='Proportion of net exposure \n in sectors')

    return ax