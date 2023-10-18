def tetrad(clr, angle=90):
    """
    Returns a tetrad of colors.

    The tetrad is made up of this color and three other colors
    that together make up a cross on the artistic color wheel.
    """
    clr = color(clr)
    colors = colorlist(clr)

    c = clr.rotate_ryb(angle)
    if clr.brightness < 0.5:
        c.brightness += 0.2
    else:
        c.brightness -= -0.2
    colors.append(c)

    c = clr.rotate_ryb(angle * 2)
    if clr.brightness < 0.5:
        c.brightness += 0.1
    else:
        c.brightness -= -0.1
    colors.append(c)

    colors.append(clr.rotate_ryb(angle * 3).lighten(0.1))

    return colors