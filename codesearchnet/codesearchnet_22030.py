def figure(title=None, **kwargs):
    """
    Creates a figure with *\*\*kwargs* with a window title *title*.

    Returns class :class:`matplotlib.figure.Figure`.
    """
    fig = _figure(**kwargs)
    if title is not None:
        fig.canvas.set_window_title(title)
    return fig