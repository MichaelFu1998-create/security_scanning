def disassemble_one(bytecode, pc=0, fork=DEFAULT_FORK):
    """ Disassemble a single instruction from a bytecode

        :param bytecode: the bytecode stream
        :type bytecode: str | bytes | bytearray | iterator
        :param pc: program counter of the instruction(optional)
        :type pc: int
        :param fork: fork name (optional)
        :type fork: str
        :return: an Instruction object
        :rtype: Instruction

        Example use::

            >>> print disassemble_one('\x60\x10')

    """
    instruction_table = instruction_tables[fork]
    if isinstance(bytecode, bytes):
        bytecode = bytearray(bytecode)
    if isinstance(bytecode, str):
        bytecode = bytearray(bytecode.encode('latin-1'))

    bytecode = iter(bytecode)
    try:
        opcode = next(bytecode)
    except StopIteration:
        return

    assert isinstance(opcode, int)

    instruction = copy.copy(instruction_table.get(opcode, None))
    if instruction is None:
        instruction = Instruction(opcode, 'INVALID', 0, 0, 0, 0, 'Unspecified invalid instruction.')
    instruction.pc = pc

    try:
        if instruction.has_operand:
            instruction.parse_operand(bytecode)
    except ParseError:
        instruction = None
    finally:
        return instruction