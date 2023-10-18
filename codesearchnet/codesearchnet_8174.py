def fill_triangle(setter, x0, y0, x1, y1, x2, y2, color=None, aa=False):
    """Draw solid triangle with points x0,y0 - x1,y1 - x2,y2"""
    a = b = y = last = 0

    if y0 > y1:
        y0, y1 = y1, y0
        x0, x1 = x1, x0
    if y1 > y2:
        y2, y1 = y1, y2
        x2, x1 = x1, x2
    if y0 > y1:
        y0, y1 = y1, y0
        x0, x1 = x1, x0

    if y0 == y2:  # Handle awkward all-on-same-line case as its own thing
        a = b = x0
        if x1 < a:
            a = x1
        elif x1 > b:
            b = x1
        if x2 < a:
            a = x2
        elif x2 > b:
            b = x2
            _draw_fast_hline(setter, a, y0, b - a + 1, color, aa)

    dx01 = x1 - x0
    dy01 = y1 - y0
    dx02 = x2 - x0
    dy02 = y2 - y0
    dx12 = x2 - x1
    dy12 = y2 - y1
    sa = 0
    sb = 0

    # For upper part of triangle, find scanline crossings for segments
    # 0-1 and 0-2.  If y1=y2 (flat-bottomed triangle), the scanline y1
    # is included here (and second loop will be skipped, avoiding a /0
    # error there), otherwise scanline y1 is skipped here and handled
    # in the second loop...which also avoids a /0 error here if y0=y1
    # (flat-topped triangle).

    if y1 == y2:
        last = y1  # include y1 scanline
    else:
        last = y1 - 1  # skip it

    for y in range(y, last + 1):
        a = x0 + sa / dy01
        b = x0 + sb / dy02
        sa += dx01
        sb += dx02

        if a > b:
            a, b = b, a
            _draw_fast_hline(setter, a, y, b - a + 1, color, aa)

    # For lower part of triangle, find scanline crossings for segments
    # 0-2 and 1-2.  This loop is skipped if y1=y2.
    sa = dx12 * (y - y1)
    sb = dx02 * (y - y0)

    for y in range(y, y2 + 1):
        a = x1 + sa / dy12
        b = x0 + sb / dy02
        sa += dx12
        sb += dx02

        if a > b:
            a, b = b, a
            _draw_fast_hline(setter, a, y, b - a + 1, color, aa)