def average(numbers, numtype='float'):
    """
    Calculates the average or mean of a list of numbers

    Args:
        numbers: a list of integers or floating point numbers.

        numtype: string, 'decimal' or 'float'; the type of number to return.

    Returns:
        The average (mean) of the numbers as a floating point number
        or a Decimal object.

    Requires:
        The math module
    """
    if type == 'decimal':
        return Decimal(sum(numbers)) / len(numbers)
    else:
        return float(sum(numbers)) / len(numbers)