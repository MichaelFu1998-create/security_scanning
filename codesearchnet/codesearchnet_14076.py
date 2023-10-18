def guess_name(clr):
    """
    Guesses the shade and hue name of a color.

    If the given color is named in the named_colors list, return that name.
    Otherwise guess its nearest hue and shade range.
    """
    clr = Color(clr)

    if clr.is_transparent: return "transparent"
    if clr.is_black: return "black"
    if clr.is_white: return "white"
    if clr.is_black: return "black"

    for name in named_colors:
        try:
            r, g, b = named_colors[name]
        except:
            continue
        if r == clr.r and g == clr.g and b == clr.b:
            return name

    for shade in shades:
        if clr in shade:
            return shade.name + " " + clr.nearest_hue()
            break

    return clr.nearest_hue()