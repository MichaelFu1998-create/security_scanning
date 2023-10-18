def addlabel(ax=None, toplabel=None, xlabel=None, ylabel=None, zlabel=None, clabel=None, cb=None, windowlabel=None, fig=None, axes=None):
    """Adds labels to a plot."""

    if (axes is None) and (ax is not None):
        axes = ax

    if (windowlabel is not None) and (fig is not None):
        fig.canvas.set_window_title(windowlabel)

    if fig is None:
        fig = _plt.gcf()

    if fig is not None and axes is None:
        axes = fig.get_axes()
        if axes == []:
            logger.error('No axes found!')

    if axes is not None:
        if toplabel is not None:
            axes.set_title(toplabel)
        if xlabel is not None:
            axes.set_xlabel(xlabel)
        if ylabel is not None:
            axes.set_ylabel(ylabel)
        if zlabel is not None:
            axes.set_zlabel(zlabel)

    if (clabel is not None) or (cb is not None):
        if (clabel is not None) and (cb is not None):
            cb.set_label(clabel)
        else:
            if clabel is None:
                logger.error('Missing colorbar label')
            else:
                logger.error('Missing colorbar instance')