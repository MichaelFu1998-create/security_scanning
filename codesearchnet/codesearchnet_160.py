def copy_random_state(random_state, force_copy=False):
    """
    Creates a copy of a random state.

    Parameters
    ----------
    random_state : numpy.random.RandomState
        The random state to copy.

    force_copy : bool, optional
        If True, this function will always create a copy of every random
        state. If False, it will not copy numpy's default random state,
        but all other random states.

    Returns
    -------
    rs_copy : numpy.random.RandomState
        The copied random state.

    """
    if random_state == np.random and not force_copy:
        return random_state
    else:
        rs_copy = dummy_random_state()
        orig_state = random_state.get_state()
        rs_copy.set_state(orig_state)
        return rs_copy