def cubehelix_pal(start=0, rot=.4, gamma=1.0, hue=0.8,
                  light=.85, dark=.15, reverse=False):
    """
    Utility for creating continuous palette from the cubehelix system.

    This produces a colormap with linearly-decreasing (or increasing)
    brightness. That means that information will be preserved if printed to
    black and white or viewed by someone who is colorblind.

    Parameters
    ----------
    start : float (0 <= start <= 3)
        The hue at the start of the helix.
    rot : float
        Rotations around the hue wheel over the range of the palette.
    gamma : float (0 <= gamma)
        Gamma factor to emphasize darker (gamma < 1) or lighter (gamma > 1)
        colors.
    hue : float (0 <= hue <= 1)
        Saturation of the colors.
    dark : float (0 <= dark <= 1)
        Intensity of the darkest color in the palette.
    light : float (0 <= light <= 1)
        Intensity of the lightest color in the palette.
    reverse : bool
        If True, the palette will go from dark to light.

    Returns
    -------
    out : function
        Continuous color palette that takes a single
        :class:`int` parameter ``n`` and returns ``n``
        equally spaced colors.


    References
    ----------
    Green, D. A. (2011). "A colour scheme for the display of astronomical
    intensity images". Bulletin of the Astromical Society of India, Vol. 39,
    p. 289-295.

    Examples
    --------
    >>> palette = cubehelix_pal()
    >>> palette(5)
    ['#edd1cb', '#d499a7', '#aa688f', '#6e4071', '#2d1e3e']
    """
    cdict = mpl._cm.cubehelix(gamma, start, rot, hue)
    cubehelix_cmap = mpl.colors.LinearSegmentedColormap('cubehelix', cdict)

    def cubehelix_palette(n):
        values = np.linspace(light, dark, n)
        return [mcolors.rgb2hex(cubehelix_cmap(x)) for x in values]

    return cubehelix_palette