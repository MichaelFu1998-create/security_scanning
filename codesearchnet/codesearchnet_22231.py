def plot(*args, ax=None, **kwargs):
    """
    Plots but automatically resizes x axis.

    .. versionadded:: 1.4

    Parameters
    ----------
    args
        Passed on to :meth:`matplotlib.axis.Axis.plot`.
    ax : :class:`matplotlib.axis.Axis`, optional
        The axis to plot to.
    kwargs
        Passed on to :meth:`matplotlib.axis.Axis.plot`.

    """
    if ax is None:
        fig, ax = _setup_axes()

    pl = ax.plot(*args, **kwargs)

    if _np.shape(args)[0] > 1:
        if type(args[1]) is not str:
            min_x = min(args[0])
            max_x = max(args[0])
            ax.set_xlim((min_x, max_x))

    return pl