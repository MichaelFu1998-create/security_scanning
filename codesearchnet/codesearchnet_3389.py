def ASR_C(value, amount, width):
    """
    The ARM ASR_C (arithmetic shift right with carry) operation.

    :param value: Value to shift
    :type value: int or long or BitVec
    :param int amount: How many bits to shift it.
    :param int width: Width of the value
    :return: Resultant value and carry result
    :rtype tuple
    """
    assert amount <= width
    assert amount > 0
    assert amount + width <= width * 2
    value = Operators.SEXTEND(value, width, width * 2)
    result = GetNBits(value >> amount, width)
    carry = Bit(value, amount - 1)
    return (result, carry)