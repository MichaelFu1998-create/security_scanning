def split_complementary(clr):
    """
    Returns a list with the split complement of the color.

    The split complement are the two colors to the left and right
    of the color's complement.
    """
    clr = color(clr)
    colors = colorlist(clr)
    clr = clr.complement
    colors.append(clr.rotate_ryb(-30).lighten(0.1))
    colors.append(clr.rotate_ryb(30).lighten(0.1))

    return colors