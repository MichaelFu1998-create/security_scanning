def _find_zero(cpu, constrs, ptr):
    """
    Helper for finding the closest NULL or, effectively NULL byte from a starting address.

    :param Cpu cpu:
    :param ConstraintSet constrs: Constraints for current `State`
    :param int ptr: Address to start searching for a zero from
    :return: Offset from `ptr` to first byte that is 0 or an `Expression` that must be zero
    """

    offset = 0
    while True:
        byt = cpu.read_int(ptr + offset, 8)

        if issymbolic(byt):
            if not solver.can_be_true(constrs, byt != 0):
                break
        else:
            if byt == 0:
                break

        offset += 1

    return offset