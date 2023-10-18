def get_algorithm(alg: str) -> Callable:
    """
    :param alg: The name of the requested `JSON Web Algorithm <https://tools.ietf.org/html/rfc7519#ref-JWA>`_. `RFC7518 <https://tools.ietf.org/html/rfc7518#section-3.2>`_ is related.
    :type alg: str
    :return: The requested algorithm.
    :rtype: Callable
    :raises: ValueError
    """
    if alg not in algorithms:
        raise ValueError('Invalid algorithm: {:s}'.format(alg))
    return algorithms[alg]