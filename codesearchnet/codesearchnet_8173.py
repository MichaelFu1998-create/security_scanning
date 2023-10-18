def draw_triangle(setter, x0, y0, x1, y1, x2, y2, color=None, aa=False):
    """Draw triangle with points x0,y0 - x1,y1 - x2,y2"""
    draw_line(setter, x0, y0, x1, y1, color, aa)
    draw_line(setter, x1, y1, x2, y2, color, aa)
    draw_line(setter, x2, y2, x0, y0, color, aa)