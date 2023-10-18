def gradient_n_pal(colors, values=None, name='gradientn'):
    """
    Create a n color gradient palette

    Parameters
    ----------
    colors : list
        list of colors
    values : list, optional
        list of points in the range [0, 1] at which to
        place each color. Must be the same size as
        `colors`. Default to evenly space the colors
    name : str
        Name to call the resultant MPL colormap

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
    >>> palette = gradient_n_pal(['red', 'blue'])
    >>> palette([0, .25, .5, .75, 1])
    ['#ff0000', '#bf0040', '#7f0080', '#3f00c0', '#0000ff']
    """
    # Note: For better results across devices and media types,
    # it would be better to do the interpolation in
    # Lab color space.
    if values is None:
        colormap = mcolors.LinearSegmentedColormap.from_list(
            name, colors)
    else:
        colormap = mcolors.LinearSegmentedColormap.from_list(
            name, list(zip(values, colors)))

    def _gradient_n_pal(vals):
        return ratios_to_colors(vals, colormap)

    return _gradient_n_pal