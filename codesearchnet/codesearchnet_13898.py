def point_in_polygon(points, x, y):
    """ Ray casting algorithm.
        Determines how many times a horizontal ray starting from the point
        intersects with the sides of the polygon.
        If it is an even number of times, the point is outside, if odd, inside.
        The algorithm does not always report correctly when the point is very close to the boundary.
        The polygon is passed as a list of (x,y)-tuples.
    """
    odd = False
    n = len(points)
    for i in range(n):
        j = i < n - 1 and i + 1 or 0
        x0, y0 = points[i][0], points[i][1]
        x1, y1 = points[j][0], points[j][1]
        if (y0 < y and y1 >= y) or (y1 < y and y0 >= y):
            if x0 + (y - y0) / (y1 - y0) * (x1 - x0) < x:
                odd = not odd
    return odd