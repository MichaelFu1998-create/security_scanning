def regular_polygon_area(number_of_sides, length_of_sides):
    """
    Calculates the area of a regular polygon (with sides of equal length).

    Args:
        number_of_sides: Integer, the number of sides of the polygon

        length_of_sides: Integer or floating point number, the length of the sides

    Returns:
        The area of a regular polygon as an integer or floating point number

    Requires:
        The math module
    """
    return (0.25 * number_of_sides * length_of_sides ** 2) / math.tan(
        math.pi / number_of_sides
    )