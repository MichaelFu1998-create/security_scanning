def random_combination(nsets, n, k):
    """
    Returns nsets unique random quartet sets sampled from
    n-choose-k without replacement combinations.
    """
    sets = set()
    while len(sets) < nsets:
        newset = tuple(sorted(np.random.choice(n, k, replace=False)))
        sets.add(newset)
    return tuple(sets)