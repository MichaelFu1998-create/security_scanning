def fill_rect(setter, x, y, w, h, color=None, aa=False):
    """Draw solid rectangle with top-left corner at x,y, width w and height h"""
    for i in range(x, x + w):
        _draw_fast_vline(setter, i, y, h, color, aa)