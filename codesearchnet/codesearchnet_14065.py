def complement(clr):
    """
    Returns the color and its complement in a list.
    """
    clr = color(clr)
    colors = colorlist(clr)
    colors.append(clr.complement)

    return colors