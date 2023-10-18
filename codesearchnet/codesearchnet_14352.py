def desaturate_pal(color, prop, reverse=False):
    """
    Create a palette that desaturate a color by some proportion

    Parameters
    ----------
    color : matplotlib color
        hex, rgb-tuple, or html color name
    prop : float
        saturation channel of color will be multiplied by
        this value
    reverse : bool
        Whether to reverse the palette.

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
    >>> palette = desaturate_pal('red', .1)
    >>> palette([0, .25, .5, .75, 1])
    ['#ff0000', '#e21d1d', '#c53a3a', '#a95656', '#8c7373']
    """
    if not 0 <= prop <= 1:
        raise ValueError("prop must be between 0 and 1")

    # Get rgb tuple rep
    # Convert to hls
    # Desaturate the saturation channel
    # Convert back to rgb
    rgb = mcolors.colorConverter.to_rgb(color)
    h, l, s = colorsys.rgb_to_hls(*rgb)
    s *= prop
    desaturated_color = colorsys.hls_to_rgb(h, l, s)
    colors = [color, desaturated_color]
    if reverse:
        colors = colors[::-1]
    return gradient_n_pal(colors, name='desaturated')