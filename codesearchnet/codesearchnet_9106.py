def assemble_all(asmcode, pc=0, fork=DEFAULT_FORK):
    """ Assemble a sequence of textual representation of EVM instructions

        :param asmcode: assembly code for any number of instructions
        :type asmcode: str
        :param pc: program counter of the first instruction(optional)
        :type pc: int
        :param fork: fork name (optional)
        :type fork: str
        :return: An generator of Instruction objects
        :rtype: generator[Instructions]

        Example use::

            >>> assemble_one('''PUSH1 0x60\n \
                            PUSH1 0x40\n \
                            MSTORE\n \
                            PUSH1 0x2\n \
                            PUSH2 0x108\n \
                            PUSH1 0x0\n \
                            POP\n \
                            SSTORE\n \
                            PUSH1 0x40\n \
                            MLOAD\n \
                            ''')

    """
    asmcode = asmcode.split('\n')
    asmcode = iter(asmcode)
    for line in asmcode:
        if not line.strip():
            continue
        instr = assemble_one(line, pc=pc, fork=fork)
        yield instr
        pc += instr.size