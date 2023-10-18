def LSL_C(value, amount, width):
    """
    The ARM LSL_C (logical left shift with carry) operation.

    :param value: Value to shift
    :type value: int or long or BitVec
    :param int amount: How many bits to shift it.
    :param int width: Width of the value
    :return: Resultant value and the carry result
    :rtype tuple
    """
    assert amount > 0
    value = Operators.ZEXTEND(value, width * 2)
    shifted = value << amount
    result = GetNBits(shifted, width)
    carry = Bit(shifted, width)
    return (result, carry)