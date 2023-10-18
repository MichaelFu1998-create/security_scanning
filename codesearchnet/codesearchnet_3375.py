def strlen(state, s):
    """
    strlen symbolic model.

    Algorithm: Walks from end of string not including NULL building ITE tree when current byte is symbolic.

    :param State state: current program state
    :param int s: Address of string
    :return: Symbolic strlen result
    :rtype: Expression or int
    """

    cpu = state.cpu

    if issymbolic(s):
        raise ConcretizeArgument(state.cpu, 1)

    zero_idx = _find_zero(cpu, state.constraints, s)

    ret = zero_idx

    for offset in range(zero_idx - 1, -1, -1):
        byt = cpu.read_int(s + offset, 8)
        if issymbolic(byt):
            ret = ITEBV(cpu.address_bit_size, byt == 0, offset, ret)

    return ret