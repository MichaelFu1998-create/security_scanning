def imshow(X, ax=None, add_cbar=True, rescale_fig=True, **kwargs):
    """
    Plots an array *X* such that the first coordinate is the *x* coordinate and the second coordinate is the *y* coordinate, with the origin at the bottom left corner.

    Optional argument *ax* allows an existing axes to be used.

    *\*\*kwargs* are passed on to :meth:`matplotlib.axes.Axes.imshow`.

    .. versionadded:: 1.3

    Returns
    -------
    fig, ax, im :
        if axes aren't specified.
    im :
        if axes are specified.
    """
    return _plot_array(X, plottype=_IMSHOW, ax=ax, add_cbar=add_cbar, rescale_fig=rescale_fig, **kwargs)