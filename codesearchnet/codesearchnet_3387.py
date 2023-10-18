def LSR_C(value, amount, width):
    """
    The ARM LSR_C (logical shift right with carry) operation.

    :param value: Value to shift
    :type value: int or long or BitVec
    :param int amount: How many bits to shift it.
    :param int width: Width of the value
    :return: Resultant value and carry result
    :rtype tuple
    """
    assert amount > 0
    result = GetNBits(value >> amount, width)
    carry = Bit(value >> (amount - 1), 0)
    return (result, carry)