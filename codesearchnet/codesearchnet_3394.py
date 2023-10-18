def RRX(value, carry, width):
    """
    The ARM RRX (rotate right with extend) operation.

    :param value: Value to shift
    :type value: int or long or BitVec
    :param int amount: How many bits to rotate it.
    :param int width: Width of the value
    :return: Resultant value
    :rtype int or BitVec
    """
    result, _ = RRX_C(value, carry, width)
    return result