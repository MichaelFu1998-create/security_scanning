def derive_random_states(random_state, n=1):
    """
    Create N new random states based on an existing random state or seed.

    Parameters
    ----------
    random_state : numpy.random.RandomState
        Random state or seed from which to derive new random states.

    n : int, optional
        Number of random states to derive.

    Returns
    -------
    list of numpy.random.RandomState
        Derived random states.

    """
    seed_ = random_state.randint(SEED_MIN_VALUE, SEED_MAX_VALUE, 1)[0]
    return [new_random_state(seed_+i) for i in sm.xrange(n)]