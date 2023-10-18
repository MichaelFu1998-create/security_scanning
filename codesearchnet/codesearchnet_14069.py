def right_complement(clr):
    """
    Returns the right half of the split complement.
    """
    right = split_complementary(clr)[2]
    colors = complementary(clr)
    colors[3].h = right.h
    colors[4].h = right.h
    colors[5].h = right.h

    colors = colorlist(
        colors[0], colors[2], colors[1], colors[5], colors[4], colors[3]
    )

    return colors