def hue_pal(h=.01, l=.6, s=.65, color_space='hls'):
    """
    Utility for making hue palettes for color schemes.

    Parameters
    ----------
    h : float
        first hue. In the [0, 1] range
    l : float
        lightness. In the [0, 1] range
    s : float
        saturation. In the [0, 1] range
    color_space : 'hls' | 'husl'
        Color space to use for the palette

    Returns
    -------
    out : function
        A discrete color palette that takes a single
        :class:`int` parameter ``n`` and returns ``n``
        equally spaced colors. Though the palette
        is continuous, since it is varies the hue it
        is good for categorical data. However if ``n``
        is large enough the colors show continuity.

    Examples
    --------
    >>> hue_pal()(5)
    ['#db5f57', '#b9db57', '#57db94', '#5784db', '#c957db']
    >>> hue_pal(color_space='husl')(5)
    ['#e0697e', '#9b9054', '#569d79', '#5b98ab', '#b675d7']
    """
    if not all([0 <= val <= 1 for val in (h, l, s)]):
        msg = ("hue_pal expects values to be between 0 and 1. "
               " I got h={}, l={}, s={}".format(h, l, s))
        raise ValueError(msg)

    if color_space not in ('hls', 'husl'):
        msg = "color_space should be one of ['hls', 'husl']"
        raise ValueError(msg)

    name = '{}_palette'.format(color_space)
    palette = globals()[name]

    def _hue_pal(n):
        colors = palette(n, h=h, l=l, s=s)
        return [mcolors.rgb2hex(c) for c in colors]

    return _hue_pal