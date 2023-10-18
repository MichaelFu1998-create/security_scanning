def triad(clr, angle=120):
    """
    Returns a triad of colors.

    The triad is made up of this color and two other colors
    that together make up an equilateral triangle on
    the artistic color wheel.
    """
    clr = color(clr)
    colors = colorlist(clr)
    colors.append(clr.rotate_ryb(angle).lighten(0.1))
    colors.append(clr.rotate_ryb(-angle).lighten(0.1))

    return colors