def husl_palette(n_colors=6, h=.01, s=.9, l=.65):
    """
    Get a set of evenly spaced colors in HUSL hue space.

    h, s, and l should be between 0 and 1

    Parameters
    ----------

    n_colors : int
        number of colors in the palette
    h : float
        first hue
    s : float
        saturation
    l : float
        lightness

    Returns
    -------
    palette : list
        List of colors as RGB hex strings.

    See Also
    --------
    hls_palette : Make a palette using evenly spaced circular
        hues in the HSL system.

    Examples
    --------
    >>> len(husl_palette(3))
    3
    >>> len(husl_palette(11))
    11
    """
    hues = np.linspace(0, 1, n_colors + 1)[:-1]
    hues += h
    hues %= 1
    hues *= 359
    s *= 99
    l *= 99
    palette = [husl.husl_to_rgb(h_i, s, l) for h_i in hues]
    return palette