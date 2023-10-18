def outline(path, colors, precision=0.4, continuous=True):
    """
    Outlines each contour in a path with the colors in the list.

    Each contour starts with the first color in the list,
    and ends with the last color in the list.

    Because each line segment is drawn separately,
    works only with corner-mode transforms.
    """
    # The count of points in a given path/contour.
    def _point_count(path, precision):
        return max(int(path.length * precision * 0.5), 10)

    # The total count of points in the path.
    n = sum([_point_count(contour, precision) for contour in path.contours])

    # For a continuous gradient,
    # we need to calculate a subrange in the list of colors
    # for each contour to draw colors from.
    contour_i = 0
    contour_n = len(path.contours) - 1
    if contour_n == 0: continuous = False

    i = 0
    for contour in path.contours:

        if not continuous: i = 0

        # The number of points for each contour.
        j = _point_count(contour, precision)

        first = True
        for pt in contour.points(j):
            if first:
                first = False
            else:
                if not continuous:
                    # If we have a list of 100 colors and 50 points,
                    # point i maps to color i*2.
                    clr = float(i) / j * len(colors)
                else:
                    # In a continuous gradient of 100 colors,
                    # the 2nd contour in a path with 10 contours
                    # draws colors between 10-20
                    clr = float(i) / n * len(colors) - 1 * contour_i / contour_n
                _ctx.stroke(colors[int(clr)])
                _ctx.line(x0, y0, pt.x, pt.y)
            x0 = pt.x
            y0 = pt.y
            i += 1

        pt = contour.point(0.9999999)  # Fix in pathmatics!
        _ctx.line(x0, y0, pt.x, pt.y)
        contour_i += 1