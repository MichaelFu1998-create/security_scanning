def bresenham_line(setter, x0, y0, x1, y1, color=None, colorFunc=None):
    """Draw line from point x0,y0 to x,1,y1. Will draw beyond matrix bounds."""
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = abs(y1 - y0)

    err = dx / 2

    if y0 < y1:
        ystep = 1
    else:
        ystep = -1

    count = 0
    for x in range(x0, x1 + 1):
        if colorFunc:
            color = colorFunc(count)
            count += 1

        if steep:
            setter(y0, x, color)
        else:
            setter(x, y0, color)

        err -= dy
        if err < 0:
            y0 += ystep
            err += dx