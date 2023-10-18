def ratios_to_colors(values, colormap):
    """
    Map values in the range [0, 1] onto colors

    Parameters
    ----------
    values : array_like | float
        Numeric(s) in the range [0, 1]
    colormap : cmap
        Matplotlib colormap to use for the mapping

    Returns
    -------
    out : list | float
        Color(s) corresponding to the values
    """
    iterable = True
    try:
        iter(values)
    except TypeError:
        iterable = False
        values = [values]

    color_tuples = colormap(values)
    try:
        hex_colors = [mcolors.rgb2hex(t) for t in color_tuples]
    except IndexError:
        hex_colors = mcolors.rgb2hex(color_tuples)
    return hex_colors if iterable else hex_colors[0]