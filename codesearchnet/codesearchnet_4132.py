def calc_list_average(l):
    """
    Calculates the average value of a list of numbers
    Returns a float
    """
    total = 0.0
    for value in l:
        total += value
    return total / len(l)