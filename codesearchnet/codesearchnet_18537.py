def variance(numbers, type='population'):
    """
    Calculates the population or sample variance of a list of numbers.
    A large number means the results are all over the place, while a
    small number means the results are comparatively close to the average.

    Args:
        numbers: a list  of integers or floating point numbers to compare.

        type: string, 'population' or 'sample', the kind of variance to be computed.

    Returns:
        The computed population or sample variance.
        Defaults to population variance.

    Requires:
        The math module, average()
    """
    mean = average(numbers)
    variance = 0
    for number in numbers:
        variance += (mean - number) ** 2

    if type == 'population':
        return variance / len(numbers)
    else:
        return variance / (len(numbers) - 1)