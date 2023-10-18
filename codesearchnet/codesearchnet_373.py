def plot_cap_exposures_net(net_exposures, ax=None):
    """
    Plots outputs of compute_cap_exposures as line graphs

    Parameters
    ----------
    net_exposures : array
        Arrays of gross market cap exposures (output of compute_cap_exposures).
    """

    if ax is None:
        ax = plt.gca()

    color_list = plt.cm.gist_rainbow(np.linspace(0, 1, 5))

    cap_names = CAP_BUCKETS.keys()
    for i in range(len(net_exposures)):
        ax.plot(net_exposures[i], color=color_list[i], alpha=0.8,
                label=cap_names[i])
    ax.axhline(0, color='k', linestyle='-')
    ax.set(title='Net exposure to market caps',
           ylabel='Proportion of net exposure \n in market cap buckets')

    return ax