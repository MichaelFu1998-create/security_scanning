def permutations_with_replacement(iterable, r=None):
    """Return successive r length permutations of elements in the iterable.

    Similar to itertools.permutation but withouth repeated values filtering.
    """
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in itertools.product(range(n), repeat=r):
        yield list(pool[i] for i in indices)