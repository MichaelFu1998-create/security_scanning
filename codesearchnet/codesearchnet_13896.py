def line_line_intersection(x1, y1, x2, y2, x3, y3, x4, y4, infinite=False):
    """ Determines the intersection point of two lines, or two finite line segments if infinite=False.
        When the lines do not intersect, returns an empty list.
    """
    # Based on: P. Bourke, http://local.wasp.uwa.edu.au/~pbourke/geometry/lineline2d/
    ua = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
    ub = (x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)
    d = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if d == 0:
        if ua == ub == 0:
            # The lines are coincident
            return []
        else:
            # The lines are parallel.
            return []
    ua /= float(d)
    ub /= float(d)
    if not infinite and not (0 <= ua <= 1 and 0 <= ub <= 1):
        # Intersection point is not within both line segments.
        return None, None
    return [(x1 + ua * (x2 - x1),
             y1 + ua * (y2 - y1))]