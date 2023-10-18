def colorbar(ax, im, fig=None, loc="right", size="5%", pad="3%"):
    """
    Adds a polite colorbar that steals space so :func:`matplotlib.pyplot.tight_layout` works nicely.

    .. versionadded:: 1.3

    Parameters
    ----------

    ax : :class:`matplotlib.axis.Axis`
        The axis to plot to.
    im : :class:`matplotlib.image.AxesImage`
        The plotted image to use for the colorbar.
    fig : :class:`matplotlib.figure.Figure`, optional
        The figure to plot to.
    loc : str, optional
        The location to place the axes.
    size : str, optional
        The size to allocate for the colorbar.
    pad : str, optional
        The amount to pad the colorbar.

    """
    if fig is None:
        fig = ax.get_figure()

    # _pdb.set_trace()
    if loc == "left" or loc == "right":
        width = fig.get_figwidth()
        new = width * (1 + _pc2f(size) + _pc2f(pad))
        _logger.debug('Setting new figure width: {}'.format(new))
        # fig.set_size_inches(new, fig.get_figheight(), forward=True)
    elif loc == "top" or loc == "bottom":
        height = fig.get_figheight()
        new = height * (1 + _pc2f(size) + _pc2f(pad))
        _logger.debug('Setting new figure height: {}'.format(new))
        # fig.set_figheight(fig.get_figwidth(), new, forward=True)

    divider = _ag1.make_axes_locatable(ax)
    cax = divider.append_axes(loc, size=size, pad=pad)
    return cax, _plt.colorbar(im, cax=cax)