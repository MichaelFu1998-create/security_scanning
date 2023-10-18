def ROR(value, amount, width):
    """
    The ARM ROR (rotate right) operation.

    :param value: Value to shift
    :type value: int or long or BitVec
    :param int amount: How many bits to rotate it.
    :param int width: Width of the value
    :return: Resultant value
    :rtype int or BitVec
    """
    if amount == 0:
        return value
    result, _ = ROR_C(value, amount, width)
    return result