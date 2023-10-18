def setup_figure(rows=1, cols=1, **kwargs):
    """
    Sets up a figure with a number of rows (*rows*) and columns (*cols*), *\*\*kwargs* passes through to :class:`matplotlib.figure.Figure`.

    .. versionchanged:: 1.3
       Supports *\*\*kwargs* pass-through to :class:`matplotlib.figure.Figure`.
       
    .. versionchanged:: 1.2
       Changed *gridspec_x* to *rows*, *gridspec_y* to *cols*, added *figsize* control.

    Parameters
    ----------

    rows : int
        Number of rows to create.
    cols : int
        Number of columns to create.

    Returns
    -------
    
    fig : :class:`matplotlib.figure.Figure`
        The figure.
    gs : :class:`matplotlib.gridspec.GridSpec`
        Instance with *gridspec_x* rows and *gridspec_y* columns
    """
    fig = _plt.figure(**kwargs)
    gs = _gridspec.GridSpec(rows, cols)

    return fig, gs