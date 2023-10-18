def median(data):
    """
    Calculates  the median of a list of integers or floating point numbers.

    Args:
        data: A list of integers or floating point numbers

    Returns:
        Sorts the list numerically and returns the middle number if the list has an odd number
        of items. If the list contains an even number of items the mean of the two middle numbers
        is returned.
    """
    ordered = sorted(data)
    length = len(ordered)
    if length % 2 == 0:
        return (
            ordered[math.floor(length / 2) - 1] + ordered[math.floor(length / 2)]
        ) / 2.0

    elif length % 2 != 0:
        return ordered[math.floor(length / 2)]