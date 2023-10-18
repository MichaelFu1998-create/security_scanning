def name_to_color(name):
    """
    :param str name: a string identifying a color.  It might be a color name
                     from the two lists of color names, juce and classic; or
                     it might be a list of numeric r, g, b values separated by
                     commas.
    :returns: a color as an RGB 3-tuple
    """
    def to_color(name):
        name = name.lower()
        if ',' in name:
            if name.startswith('(') and name.endswith(')'):
                name = name[1:-1]
            if name.startswith('[') and name.endswith(']'):
                name = name[1:-1]

            r, g, b = name.split(',')
            return _from_number(r), _from_number(g), _from_number(b)

        try:
            n = _from_number(name)
        except:
            color = tables.get_color(name)
            if color:
                return color
            raise ValueError

        return tables.to_triplet(n)

    try:
        color = to_color(name)
    except:
        raise ValueError('Unknown color name %s' % str(name))

    if not all(0 <= i <= 255 for i in color):
        raise ValueError('Component out of range: %s' % color)

    return color