def cmap_pal(name=None, lut=None):
    """
    Create a continuous palette using an MPL colormap

    Parameters
    ----------
    name : str
        Name of colormap
    lut : None | int
        This is the number of entries desired in the lookup table.
        Default is ``None``, leave it up Matplotlib.

    Returns
    -------
    out : function
        Continuous color palette that takes a single
        parameter either a :class:`float` or a sequence
        of floats maps those value(s) onto the palette
        and returns color(s). The float(s) must be
        in the range [0, 1].

    Examples
    --------
    >>> palette = cmap_pal('viridis')
    >>> palette([.1, .2, .3, .4, .5])
    ['#482475', '#414487', '#355f8d', '#2a788e', '#21918c']
    """
    colormap = get_cmap(name, lut)

    def _cmap_pal(vals):
        return ratios_to_colors(vals, colormap)

    return _cmap_pal