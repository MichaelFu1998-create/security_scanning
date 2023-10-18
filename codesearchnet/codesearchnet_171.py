def compute_line_intersection_point(x1, y1, x2, y2, x3, y3, x4, y4):
    """
    Compute the intersection point of two lines.

    Taken from https://stackoverflow.com/a/20679579 .

    Parameters
    ----------
    x1 : number
        x coordinate of the first point on line 1. (The lines extends beyond this point.)

    y1 : number
        y coordinate of the first point on line 1. (The lines extends beyond this point.)

    x2 : number
        x coordinate of the second point on line 1. (The lines extends beyond this point.)

    y2 : number
        y coordinate of the second point on line 1. (The lines extends beyond this point.)

    x3 : number
        x coordinate of the first point on line 2. (The lines extends beyond this point.)

    y3 : number
        y coordinate of the first point on line 2. (The lines extends beyond this point.)

    x4 : number
        x coordinate of the second point on line 2. (The lines extends beyond this point.)

    y4 : number
        y coordinate of the second point on line 2. (The lines extends beyond this point.)

    Returns
    -------
    tuple of number or bool
        The coordinate of the intersection point as a tuple ``(x, y)``.
        If the lines are parallel (no intersection point or an infinite number of them), the result is False.

    """
    def _make_line(p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])
        return A, B, -C

    L1 = _make_line((x1, y1), (x2, y2))
    L2 = _make_line((x3, y3), (x4, y4))

    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False