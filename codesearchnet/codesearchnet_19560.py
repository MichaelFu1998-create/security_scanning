def np_seed(seed):
    """
    numpy random seed context
    :param seed:
    :return:
    """
    if seed is not None:
        state = np.random.get_state()
        np.random.seed(seed)
        yield
        np.random.set_state(state)

    else:
        yield