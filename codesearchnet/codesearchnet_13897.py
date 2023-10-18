def circle_line_intersection(cx, cy, radius, x1, y1, x2, y2, infinite=False):
    """ Returns a list of points where the circle and the line intersect.
            Returns an empty list when the circle and the line do not intersect.
    """
    # Based on: http://www.vb-helper.com/howto_net_line_circle_intersections.html
    dx = x2 - x1
    dy = y2 - y1
    A = dx * dx + dy * dy
    B = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
    C = pow(x1 - cx, 2) + pow(y1 - cy, 2) - radius * radius
    det = B * B - 4 * A * C
    if A <= 0.0000001 or det < 0:
        return []
    elif det == 0:
        # One point of intersection.
        t = -B / (2 * A)
        return [(x1 + t * dx, y1 + t * dy)]
    else:
        # Two points of intersection.
        # A point of intersection lies on the line segment if 0 <= t <= 1,
        # and on an extension of the segment otherwise.
        points = []
        det2 = sqrt(det)
        t1 = (-B + det2) / (2 * A)
        t2 = (-B - det2) / (2 * A)
        if infinite or 0 <= t1 <= 1:
            points.append((x1 + t1 * dx, y1 + t1 * dy))
        if infinite or 0 <= t2 <= 1:
            points.append((x1 + t2 * dx, y1 + t2 * dy))
        return points