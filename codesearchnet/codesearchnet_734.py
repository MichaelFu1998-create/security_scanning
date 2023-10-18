def sample(a=None, temperature=1.0):
    """Sample an index from a probability array.

    Parameters
    ----------
    a : list of float
        List of probabilities.
    temperature : float or None
        The higher the more uniform. When a = [0.1, 0.2, 0.7],
            - temperature = 0.7, the distribution will be sharpen [0.05048273,  0.13588945,  0.81362782]
            - temperature = 1.0, the distribution will be the same [0.1,    0.2,    0.7]
            - temperature = 1.5, the distribution will be filtered [0.16008435,  0.25411807,  0.58579758]
            - If None, it will be ``np.argmax(a)``

    Notes
    ------
    - No matter what is the temperature and input list, the sum of all probabilities will be one. Even if input list = [1, 100, 200], the sum of all probabilities will still be one.
    - For large vocabulary size, choice a higher temperature or ``tl.nlp.sample_top`` to avoid error.

    """
    if a is None:
        raise Exception("a : list of float")
    b = np.copy(a)
    try:
        if temperature == 1:
            return np.argmax(np.random.multinomial(1, a, 1))
        if temperature is None:
            return np.argmax(a)
        else:
            a = np.log(a) / temperature
            a = np.exp(a) / np.sum(np.exp(a))
            return np.argmax(np.random.multinomial(1, a, 1))
    except Exception:
        # np.set_printoptions(threshold=np.nan)
        # tl.logging.info(a)
        # tl.logging.info(np.sum(a))
        # tl.logging.info(np.max(a))
        # tl.logging.info(np.min(a))
        # exit()
        message = "For large vocabulary_size, choice a higher temperature\
         to avoid log error. Hint : use ``sample_top``. "

        warnings.warn(message, Warning)
        # tl.logging.info(a)
        # tl.logging.info(b)
        return np.argmax(np.random.multinomial(1, b, 1))