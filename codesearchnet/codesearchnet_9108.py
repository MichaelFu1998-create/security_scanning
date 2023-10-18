def disassemble_all(bytecode, pc=0, fork=DEFAULT_FORK):
    """ Disassemble all instructions in bytecode

        :param bytecode: an evm bytecode (binary)
        :type bytecode: str | bytes | bytearray | iterator
        :param pc: program counter of the first instruction(optional)
        :type pc: int
        :param fork: fork name (optional)
        :type fork: str
        :return: An generator of Instruction objects
        :rtype: list[Instruction]

        Example use::

            >>> for inst in disassemble_all(bytecode):
            ...    print(instr)

            ...
            PUSH1 0x60
            PUSH1 0x40
            MSTORE
            PUSH1 0x2
            PUSH2 0x108
            PUSH1 0x0
            POP
            SSTORE
            PUSH1 0x40
            MLOAD


    """
    if isinstance(bytecode, bytes):
        bytecode = bytearray(bytecode)
    if isinstance(bytecode, str):
        bytecode = bytearray(bytecode.encode('latin-1'))

    bytecode = iter(bytecode)
    while True:
        instr = disassemble_one(bytecode, pc=pc, fork=fork)
        if not instr:
            return
        pc += instr.size
        yield instr