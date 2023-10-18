def draw_rect(setter, x, y, w, h, color=None, aa=False):
    """Draw rectangle with top-left corner at x,y, width w and height h"""
    _draw_fast_hline(setter, x, y, w, color, aa)
    _draw_fast_hline(setter, x, y + h - 1, w, color, aa)
    _draw_fast_vline(setter, x, y, h, color, aa)
    _draw_fast_vline(setter, x + w - 1, y, h, color, aa)