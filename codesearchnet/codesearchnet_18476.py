def compare_signature(expected: Union[str, bytes],
                      actual: Union[str, bytes]) -> bool:
    """
    Compares the given signatures.

    :param expected: The expected signature.
    :type expected: Union[str, bytes]
    :param actual: The actual signature.
    :type actual: Union[str, bytes]
    :return: Do the signatures match?
    :rtype: bool
    """
    expected = util.to_bytes(expected)
    actual = util.to_bytes(actual)
    return hmac.compare_digest(expected, actual)