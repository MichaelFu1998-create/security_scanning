def fill_round_rect(setter, x, y, w, h, r, color=None, aa=False):
    """Draw solid rectangle with top-left corner at x,y, width w, height h,
    and corner radius r"""
    fill_rect(setter, x + r, y, w - 2 * r, h, color, aa)
    _fill_circle_helper(setter, x + w - r - 1, y + r, r,
                        1, h - 2 * r - 1, color, aa)
    _fill_circle_helper(setter, x + r, y + r, r, 2, h - 2 * r - 1, color, aa)