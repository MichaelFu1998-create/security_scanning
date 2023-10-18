def hist(x, bins=10, labels=None, aspect="auto", plot=True, ax=None, range=None):
    """
    Creates a histogram of data *x* with a *bins*, *labels* = :code:`[title, xlabel, ylabel]`.
    """

    h, edge = _np.histogram(x, bins=bins, range=range)
    
    mids = edge + (edge[1]-edge[0])/2
    mids = mids[:-1]

    if plot:
        if ax is None:
            _plt.hist(x, bins=bins, range=range)
        else:
            ax.hist(x, bins=bins, range=range)

        if labels is not None:
            _addlabel(labels[0], labels[1], labels[2])

    return h, mids