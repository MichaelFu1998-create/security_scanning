def hist2d(x, y, bins=10, labels=None, aspect="auto", plot=True, fig=None, ax=None, interpolation='none', cbar=True, **kwargs):
    """
    Creates a 2-D histogram of data *x*, *y* with *bins*, *labels* = :code:`[title, xlabel, ylabel]`, aspect ration *aspect*. Attempts to use axis *ax* first, then the current axis of *fig*, then the last axis, to use an already-created window.
    
    Plotting (*plot*) is on by default, setting false doesn't attempt to create a figure.

    *interpolation* sets the interpolation type of :meth:`matplotlib.axis.imshow`.

    Returns a handle and extent as :code:`h, extent`
    """
    h_range   = kwargs.pop('range', None)
    h_normed  = kwargs.pop('normed', None)
    h_weights = kwargs.pop('weights', None)

    h, xe, ye = _np.histogram2d(x, y, bins=bins, range=h_range, normed=h_normed, weights=h_weights)
    extent    = [xe[0], xe[-1], ye[0], ye[-1]]
    # fig     = plt.figure()
    if plot:
        if ax is None:
            if fig is None:
                fig = _figure('hist2d')
            ax = fig.gca()
            ax.clear()

        img = ax.imshow(h.transpose(), extent=extent, interpolation=interpolation, aspect=aspect, **kwargs)
        if cbar:
            _colorbar(ax=ax, im=img)

        if labels is not None:
            _addlabel(labels[0], labels[1], labels[2])

        # _showfig(fig, aspect)
    return h, extent