def ROR_C(value, amount, width):
    """
    The ARM ROR_C (rotate right with carry) operation.

    :param value: Value to shift
    :type value: int or long or BitVec
    :param int amount: How many bits to rotate it.
    :param int width: Width of the value
    :return: Resultant value and carry result
    :rtype tuple
    """
    assert amount <= width
    assert amount > 0
    m = amount % width
    right, _ = LSR_C(value, m, width)
    left, _ = LSL_C(value, width - m, width)
    result = left | right
    carry = Bit(result, width - 1)
    return (result, carry)