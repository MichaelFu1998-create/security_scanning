def draw_circle(setter, x0, y0, r, color=None):
    """
    Draws a circle at point x0, y0 with radius r of the specified RGB color
    """
    f = 1 - r
    ddF_x = 1
    ddF_y = -2 * r
    x = 0
    y = r

    setter(x0, y0 + r, color)
    setter(x0, y0 - r, color)
    setter(x0 + r, y0, color)
    setter(x0 - r, y0, color)

    while x < y:
        if f >= 0:
            y -= 1
            ddF_y += 2
            f += ddF_y
        x += 1
        ddF_x += 2
        f += ddF_x

        setter(x0 + x, y0 + y, color)
        setter(x0 - x, y0 + y, color)
        setter(x0 + x, y0 - y, color)
        setter(x0 - x, y0 - y, color)
        setter(x0 + y, y0 + x, color)
        setter(x0 - y, y0 + x, color)
        setter(x0 + y, y0 - x, color)
        setter(x0 - y, y0 - x, color)