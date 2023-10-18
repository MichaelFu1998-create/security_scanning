def draw_round_rect(setter, x, y, w, h, r, color=None, aa=False):
    """Draw rectangle with top-left corner at x,y, width w, height h,
    and corner radius r.
    """
    _draw_fast_hline(setter, x + r, y, w - 2 * r, color, aa)  # Top
    _draw_fast_hline(setter, x + r, y + h - 1, w - 2 * r, color, aa)  # Bottom
    _draw_fast_vline(setter, x, y + r, h - 2 * r, color, aa)  # Left
    _draw_fast_vline(setter, x + w - 1, y + r, h - 2 * r, color, aa)  # Right
    # draw four corners
    _draw_circle_helper(setter, x + r, y + r, r, 1, color, aa)
    _draw_circle_helper(setter, x + w - r - 1, y + r, r, 2, color, aa)
    _draw_circle_helper(setter, x + w - r - 1, y + h - r - 1, r, 4, color, aa)
    _draw_circle_helper(setter, x + r, y + h - r - 1, r, 8, color, aa)