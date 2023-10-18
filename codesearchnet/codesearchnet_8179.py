def genVector(width, height, x_mult=1, y_mult=1):
    """
    Generates a map of vector lengths from the center point to each coordinate.

    width - width of matrix to generate
    height - height of matrix to generate
    x_mult - value to scale x-axis by
    y_mult - value to scale y-axis by
    """
    center_x = (width - 1) / 2
    center_y = (height - 1) / 2

    def length(x, y):
        dx = math.pow(x - center_x, 2 * x_mult)
        dy = math.pow(y - center_y, 2 * y_mult)
        return int(math.sqrt(dx + dy))

    return [[length(x, y) for x in range(width)] for y in range(height)]