def _hash(secret: bytes, data: bytes, alg: str) -> bytes:
    """
    Create a new HMAC hash.

    :param secret: The secret used when hashing data.
    :type secret: bytes
    :param data: The data to hash.
    :type data: bytes
    :param alg: The algorithm to use when hashing `data`.
    :type alg: str
    :return: New HMAC hash.
    :rtype: bytes
    """
    algorithm = get_algorithm(alg)
    return hmac \
        .new(secret, msg=data, digestmod=algorithm) \
        .digest()