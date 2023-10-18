def colors_no_palette(colors=None, **kwds):
    """Return a Palette but don't take into account Pallete Names."""
    if isinstance(colors, str):
        colors = _split_colors(colors)
    else:
        colors = to_triplets(colors or ())

    colors = (color(c) for c in colors or ())
    return palette.Palette(colors, **kwds)