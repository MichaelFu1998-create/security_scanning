def RRX_C(value, carry, width):
    """
    The ARM RRX (rotate right with extend and with carry) operation.

    :param value: Value to shift
    :type value: int or long or BitVec
    :param int amount: How many bits to rotate it.
    :param int width: Width of the value
    :return: Resultant value and carry result
    :rtype tuple
    """
    carry_out = Bit(value, 0)
    result = (value >> 1) | (carry << (width - 1))
    return (result, carry_out)