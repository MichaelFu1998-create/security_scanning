def set_colorbar(cb_ticksize, cb_fraction, cb_pad, cb_tick_values, cb_tick_labels):
    """Setup the colorbar of the figure, specifically its ticksize and the size is appears relative to the figure.

    Parameters
    -----------
    cb_ticksize : int
        The size of the tick labels on the colorbar.
    cb_fraction : float
        The fraction of the figure that the colorbar takes up, which resizes the colorbar relative to the figure.
    cb_pad : float
        Pads the color bar in the figure, which resizes the colorbar relative to the figure.
    cb_tick_values : [float]
        Manually specified values of where the colorbar tick labels appear on the colorbar.
    cb_tick_labels : [float]
        Manually specified labels of the color bar tick labels, which appear where specified by cb_tick_values.
    """

    if cb_tick_values is None and cb_tick_labels is None:
        cb = plt.colorbar(fraction=cb_fraction, pad=cb_pad)
    elif cb_tick_values is not None and cb_tick_labels is not None:
        cb = plt.colorbar(fraction=cb_fraction, pad=cb_pad, ticks=cb_tick_values)
        cb.ax.set_yticklabels(cb_tick_labels)
    else:
        raise exc.PlottingException('Only 1 entry of cb_tick_values or cb_tick_labels was input. You must either supply'
                                    'both the values and labels, or neither.')

    cb.ax.tick_params(labelsize=cb_ticksize)