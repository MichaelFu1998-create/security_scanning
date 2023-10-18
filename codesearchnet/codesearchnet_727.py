def get_random_int(min_v=0, max_v=10, number=5, seed=None):
    """Return a list of random integer by the given range and quantity.

    Parameters
    -----------
    min_v : number
        The minimum value.
    max_v : number
        The maximum value.
    number : int
        Number of value.
    seed : int or None
        The seed for random.

    Examples
    ---------
    >>> r = get_random_int(min_v=0, max_v=10, number=5)
    [10, 2, 3, 3, 7]

    """
    rnd = random.Random()
    if seed:
        rnd = random.Random(seed)
    # return [random.randint(min,max) for p in range(0, number)]
    return [rnd.randint(min_v, max_v) for p in range(0, number)]