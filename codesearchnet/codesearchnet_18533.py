def triangle_area(point1, point2, point3):
    """
    Uses Heron's formula to find the area of a triangle
    based on the coordinates of three points.

    Args:
        point1: list or tuple, the x y coordinate of point one.

        point2: list or tuple, the x y coordinate of point two.

        point3: list or tuple, the x y coordinate of point three.

    Returns:
        The area of a triangle as a floating point number.

    Requires:
        The math module, point_distance().
    """

    """Lengths of the three sides of the triangle"""
    a = point_distance(point1, point2)
    b = point_distance(point1, point3)
    c = point_distance(point2, point3)

    """Where s is the semiperimeter"""
    s = (a + b + c) / 2.0

    """Return the area of the triangle (using Heron's formula)"""
    return math.sqrt(s * (s - a) * (s - b) * (s - c))