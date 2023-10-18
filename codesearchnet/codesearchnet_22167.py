def setup_axes(rows=1, cols=1, figsize=(8, 6), expand=True, tight_layout=None, **kwargs):
    """
    Sets up a figure of size *figsize* with a number of rows (*rows*) and columns (*cols*). \*\*kwargs passed through to :meth:`matplotlib.figure.Figure.add_subplot`.

    .. versionadded:: 1.2

    Parameters
    ----------

    rows : int
        Number of rows to create.
    cols : int
        Number of columns to create.
    figsize : tuple
        Size of figure to create.
    expand : bool
        Make the entire figure with size `figsize`.

    Returns
    -------
    
    fig : :class:`matplotlib.figure.Figure`
        The figure.
    axes : :class:`numpy.ndarray`
        An array of all of the axes. (Unless there's only one axis, in which case it returns an object instance :class:`matplotlib.axis.Axis`.)
    """

    if expand:
        figsize = (figsize[0]*cols, figsize[1]*rows)

    figargs = {}
    if isinstance(tight_layout, dict):
        figargs["tight_layout"] = tight_layout
    elif tight_layout == "pdf":
        figargs["tight_layout"] = {"rect": (0, 0, 1, 0.95)}

    dpi = kwargs.pop('dpi', None)

    fig, gs = _setup_figure(rows=rows, cols=cols, figsize=figsize, dpi=dpi, **figargs)

    axes = _np.empty(shape=(rows, cols), dtype=object)

    for i in range(rows):
        for j in range(cols):
            axes[i, j] = fig.add_subplot(gs[i, j], **kwargs)

    if axes.shape == (1, 1):
        return fig, axes[0, 0]
    else:
        return fig, axes