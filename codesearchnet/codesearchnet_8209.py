def color_to_name(color, use_hex=False):
    """
    :param tuple color: an RGB 3-tuple of integer colors
    :returns: a string name for this color

    ``name_to_color(color_to_name(c)) == c`` is guaranteed to be true (but the
    reverse is not true, because name_to_color is a many-to-one function).
    """
    if isinstance(color, list):
        color = tuple(color)
    elif not isinstance(color, tuple):
        raise ValueError('Not a color')

    if use_hex:
        return '#%02x%02x%02x' % color

    return tables.get_name(color) or str(color)