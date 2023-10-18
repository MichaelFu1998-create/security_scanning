def cmap_d_pal(name=None, lut=None):
    """
    Create a discrete palette using an MPL Listed colormap

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
        A discrete color palette that takes a single
        :class:`int` parameter ``n`` and returns ``n``
        colors. The maximum value of ``n`` varies
        depending on the parameters.

    Examples
    --------
    >>> palette = cmap_d_pal('viridis')
    >>> palette(5)
    ['#440154', '#3b528b', '#21918c', '#5cc863', '#fde725']
    """
    colormap = get_cmap(name, lut)

    if not isinstance(colormap, mcolors.ListedColormap):
        raise ValueError(
            "For a discrete palette, cmap must be of type "
            "matplotlib.colors.ListedColormap")

    ncolors = len(colormap.colors)

    def _cmap_d_pal(n):
        if n > ncolors:
            raise ValueError(
                "cmap `{}` has {} colors you requested {} "
                "colors.".format(name, ncolors, n))

        if ncolors < 256:
            return [mcolors.rgb2hex(c) for c in colormap.colors[:n]]
        else:
            # Assume these are continuous and get colors equally spaced
            # intervals  e.g. viridis is defined with 256 colors
            idx = np.linspace(0, ncolors-1, n).round().astype(int)
            return [mcolors.rgb2hex(colormap.colors[i]) for i in idx]

    return _cmap_d_pal