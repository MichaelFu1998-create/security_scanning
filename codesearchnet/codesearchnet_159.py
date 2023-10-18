def new_random_state(seed=None, fully_random=False):
    """
    Returns a new random state.

    Parameters
    ----------
    seed : None or int, optional
        Optional seed value to use.
        The same datatypes are allowed as for ``numpy.random.RandomState(seed)``.

    fully_random : bool, optional
        Whether to use numpy's random initialization for the
        RandomState (used if set to True). If False, a seed is sampled from
        the global random state, which is a bit faster and hence the default.

    Returns
    -------
    numpy.random.RandomState
        The new random state.

    """
    if seed is None:
        if not fully_random:
            # sample manually a seed instead of just RandomState(),
            # because the latter one
            # is way slower.
            seed = CURRENT_RANDOM_STATE.randint(SEED_MIN_VALUE, SEED_MAX_VALUE, 1)[0]
    return np.random.RandomState(seed)