def hls_palette(n_colors=6, h=.01, l=.6, s=.65):
    """
    Get a set of evenly spaced colors in HLS hue space.

    h, l, and s should be between 0 and 1

    Parameters
    ----------

    n_colors : int
        number of colors in the palette
    h : float
        first hue
    l : float
        lightness
    s : float
        saturation

    Returns
    -------
    palette : list
        List of colors as RGB hex strings.

    See Also
    --------
    husl_palette : Make a palette using evenly spaced circular
        hues in the HUSL system.

    Examples
    --------
    >>> len(hls_palette(2))
    2
    >>> len(hls_palette(9))
    9
    """
    hues = np.linspace(0, 1, n_colors + 1)[:-1]
    hues += h
    hues %= 1
    hues -= hues.astype(int)
    palette = [colorsys.hls_to_rgb(h_i, l, s) for h_i in hues]
    return palette