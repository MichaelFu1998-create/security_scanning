def brewer_pal(type='seq', palette=1):
    """
    Utility for making a brewer palette

    Parameters
    ----------
    type : 'sequential' | 'qualitative' | 'diverging'
        Type of palette. Sequential, Qualitative or
        Diverging. The following abbreviations may
        be used, ``seq``, ``qual`` or ``div``.

    palette : int | str
        Which palette to choose from. If is an integer,
        it must be in the range ``[0, m]``, where ``m``
        depends on the number sequential, qualitative or
        diverging palettes. If it is a string, then it
        is the name of the palette.

    Returns
    -------
    out : function
        A color palette that takes a single
        :class:`int` parameter ``n`` and returns ``n``
        colors. The maximum value of ``n`` varies
        depending on the parameters.

    Examples
    --------
    >>> brewer_pal()(5)
    ['#EFF3FF', '#BDD7E7', '#6BAED6', '#3182BD', '#08519C']
    >>> brewer_pal('qual')(5)
    ['#7FC97F', '#BEAED4', '#FDC086', '#FFFF99', '#386CB0']
    >>> brewer_pal('qual', 2)(5)
    ['#1B9E77', '#D95F02', '#7570B3', '#E7298A', '#66A61E']
    >>> brewer_pal('seq', 'PuBuGn')(5)
    ['#F6EFF7', '#BDC9E1', '#67A9CF', '#1C9099', '#016C59']

    The available color names for each palette type can be
    obtained using the following code::

        import palettable.colorbrewer as brewer

        print([k for k in brewer.COLOR_MAPS['Sequential'].keys()])
        print([k for k in brewer.COLOR_MAPS['Qualitative'].keys()])
        print([k for k in brewer.COLOR_MAPS['Diverging'].keys()])
    """
    def full_type_name(text):
        abbrevs = {
            'seq': 'Sequential',
            'qual': 'Qualitative',
            'div': 'Diverging'
        }
        text = abbrevs.get(text, text)
        return text.title()

    def number_to_palette_name(ctype, n):
        """
        Return palette name that corresponds to a given number

        Uses alphabetical ordering
        """
        n -= 1
        palettes = sorted(colorbrewer.COLOR_MAPS[ctype].keys())
        if n < len(palettes):
            return palettes[n]

        raise ValueError(
            "There are only '{}' palettes of type {}. "
            "You requested palette no. {}".format(len(palettes),
                                                  ctype, n+1))

    def max_palette_colors(type, palette_name):
        """
        Return the number of colors in the brewer palette
        """
        if type == 'Sequential':
            return 9
        elif type == 'Diverging':
            return 11
        else:
            # Qualitative palettes have different limits
            qlimit = {'Accent': 8, 'Dark2': 8, 'Paired': 12,
                      'Pastel1': 9, 'Pastel2': 8, 'Set1': 9,
                      'Set2': 8, 'Set3': 12}
            return qlimit[palette_name]

    type = full_type_name(type)
    if isinstance(palette, int):
        palette_name = number_to_palette_name(type, palette)
    else:
        palette_name = palette

    nmax = max_palette_colors(type, palette_name)

    def _brewer_pal(n):
        # Only draw the maximum allowable colors from the palette
        # and fill any remaining spots with None
        _n = n if n <= nmax else nmax
        try:
            bmap = colorbrewer.get_map(palette_name, type, _n)
        except ValueError as err:
            # Some palettes have a minimum no. of colors set at 3
            # We get around that restriction.
            if 0 <= _n < 3:
                bmap = colorbrewer.get_map(palette_name, type, 3)
            else:
                raise err

        hex_colors = bmap.hex_colors[:n]
        if n > nmax:
            msg = ("Warning message:"
                   "Brewer palette {} has a maximum of {} colors"
                   "Returning the palette you asked for with"
                   "that many colors".format(palette_name, nmax))
            warnings.warn(msg)
            hex_colors = hex_colors + [None] * (n - nmax)
        return hex_colors

    return _brewer_pal