def grey_pal(start=0.2, end=0.8):
    """
    Utility for creating continuous grey scale palette

    Parameters
    ----------
    start : float
        grey value at low end of palette
    end : float
        grey value at high end of palette

    Returns
    -------
    out : function
        Continuous color palette that takes a single
        :class:`int` parameter ``n`` and returns ``n``
        equally spaced colors.

    Examples
    --------
    >>> palette = grey_pal()
    >>> palette(5)
    ['#333333', '#737373', '#989898', '#b5b5b5', '#cccccc']
    """
    gamma = 2.2
    ends = ((0.0, start, start), (1.0, end, end))
    cdict = {'red': ends, 'green': ends, 'blue': ends}
    grey_cmap = mcolors.LinearSegmentedColormap('grey', cdict)

    def continuous_grey_palette(n):
        colors = []
        # The grey scale points are linearly separated in
        # gamma encoded space
        for x in np.linspace(start**gamma, end**gamma, n):
            # Map points onto the [0, 1] palette domain
            x = (x ** (1./gamma) - start) / (end - start)
            colors.append(mcolors.rgb2hex(grey_cmap(x)))
        return colors

    return continuous_grey_palette