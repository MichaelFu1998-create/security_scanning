def NonUniformImage(x, y, z, ax=None, fig=None, cmap=None, alpha=None, scalex=True, scaley=True, add_cbar=True, **kwargs):
    """
    Used to plot a set of coordinates.


    Parameters
    ----------
    x, y : :class:`numpy.ndarray`
        1-D ndarrays of lengths N and M, respectively, specifying pixel centers
    z : :class:`numpy.ndarray`
        An (M, N) ndarray or masked array of values to be colormapped, or a (M, N, 3) RGB array, or a (M, N, 4) RGBA array.
    ax : :class:`matplotlib.axes.Axes`, optional
        The axis to plot to.
    fig : :class:`matplotlib.figure.Figure`, optional
        The figure to plot to.
    cmap : :class:`matplotlib.colors.Colormap`, optional
        The colormap to use.
    alpha : float, optional
        The transparency to use.
    scalex : bool, optional
        To set the x limits to available data
    scaley : bool, optional
        To set the y limits to available data
    add_cbar : bool, optional
        Whether ot add a colorbar or not.

    Returns
    -------
    img : :class:`matplotlib.image.NonUniformImage`
        Object representing the :class:`matplotlib.image.NonUniformImage`.
    """
    if ax is None and fig is None:
        fig, ax = _setup_axes()
    elif ax is None:
        ax = fig.gca()
    elif fig is None:
        fig = ax.get_figure()

    norm = kwargs.get('norm', None)

    im = _mplim.NonUniformImage(ax, **kwargs)

    vmin = kwargs.pop('vmin', _np.min(z))
    vmax = kwargs.pop('vmax', _np.max(z))
    # im.set_clim(vmin=vmin, vmax=vmax)

    if cmap is not None:
        im.set_cmap(cmap)

    m = _cm.ScalarMappable(cmap=im.get_cmap(), norm=norm)
    m.set_array(z)

    if add_cbar:
        cax, cb = _cb(ax=ax, im=m, fig=fig)

    if alpha is not None:
        im.set_alpha(alpha)

    im.set_data(x, y, z)
    ax.images.append(im)

    if scalex:
        xmin = min(x)
        xmax = max(x)
        ax.set_xlim(xmin, xmax)

    if scaley:
        ymin = min(y)
        ymax = max(y)
        ax.set_ylim(ymin, ymax)

    return _SI(im=im, cb=cb, cax=cax)