def smoothstep(a, b, x):
    """ Returns a smooth transition between 0.0 and 1.0 using Hermite interpolation (cubic spline),
        where x is a number between a and b. The return value will ease (slow down) as x nears a or b.
        For x smaller than a, returns 0.0. For x bigger than b, returns 1.0.
    """
    if x < a:
        return 0.0
    if x >= b:
        return 1.0
    x = float(x - a) / (b - a)
    return x * x * (3 - 2 * x)