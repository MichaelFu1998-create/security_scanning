def compare_token(expected: Union[str, bytes],
                  actual: Union[str, bytes]) -> bool:
    """
    Compares the given tokens.

    :param expected: The expected token.
    :type expected: Union[str, bytes]
    :param actual: The actual token.
    :type actual: Union[str, bytes]
    :return: Do the tokens match?
    :rtype: bool
    """
    expected = util.to_bytes(expected)
    actual = util.to_bytes(actual)
    _, expected_sig_seg = expected.rsplit(b'.', 1)
    _, actual_sig_seg = actual.rsplit(b'.', 1)
    expected_sig = util.b64_decode(expected_sig_seg)
    actual_sig = util.b64_decode(actual_sig_seg)
    return compare_signature(expected_sig, actual_sig)