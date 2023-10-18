def fill_circle(setter, x0, y0, r, color=None):
    """Draws a filled circle at point x0,y0 with radius r and specified color"""
    _draw_fast_vline(setter, x0, y0 - r, 2 * r + 1, color)
    _fill_circle_helper(setter, x0, y0, r, 3, 0, color)