def make_clean_figure(figsize, remove_tooltips=False, remove_keybindings=False):
    """
    Makes a `matplotlib.pyplot.Figure` without tooltips or keybindings

    Parameters
    ----------
    figsize : tuple
        Figsize as passed to `matplotlib.pyplot.figure`
    remove_tooltips, remove_keybindings : bool
        Set to True to remove the tooltips bar or any key bindings,
        respectively. Default is False

    Returns
    -------
    fig : `matplotlib.pyplot.Figure`
    """
    tooltip = mpl.rcParams['toolbar']
    if remove_tooltips:
        mpl.rcParams['toolbar'] = 'None'
    fig = pl.figure(figsize=figsize)
    mpl.rcParams['toolbar'] = tooltip
    if remove_keybindings:
        fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)
    return fig