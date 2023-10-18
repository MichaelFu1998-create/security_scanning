def left_complement(clr):
    """
    Returns the left half of the split complement.

    A list is returned with the same darker and softer colors
    as in the complementary list, but using the hue of the
    left split complement instead of the complement itself.
    """
    left = split_complementary(clr)[1]
    colors = complementary(clr)
    colors[3].h = left.h
    colors[4].h = left.h
    colors[5].h = left.h

    colors = colorlist(
        colors[0], colors[2], colors[1], colors[3], colors[4], colors[5]
    )

    return colors