def LSL(value, amount, width):
    """
    The ARM LSL (logical left shift) operation.

    :param value: Value to shift
    :type value: int or long or BitVec
    :param int amount: How many bits to shift it.
    :param int width: Width of the value
    :return: Resultant value
    :rtype int or BitVec
    """
    if amount == 0:
        return value

    result, _ = LSL_C(value, amount, width)
    return result