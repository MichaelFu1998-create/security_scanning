def assemble_one(asmcode, pc=0, fork=DEFAULT_FORK):
    """ Assemble one EVM instruction from its textual representation.

        :param asmcode: assembly code for one instruction
        :type asmcode: str
        :param pc: program counter of the instruction(optional)
        :type pc: int
        :param fork: fork name (optional)
        :type fork: str
        :return: An Instruction object
        :rtype: Instruction

        Example use::

            >>> print assemble_one('LT')


    """
    try:
        instruction_table = instruction_tables[fork]
        asmcode = asmcode.strip().split(' ')
        instr = instruction_table[asmcode[0].upper()]
        if pc:
            instr.pc = pc
        if instr.operand_size > 0:
            assert len(asmcode) == 2
            instr.operand = int(asmcode[1], 0)
        return instr
    except:
        raise AssembleError("Something wrong at pc %d" % pc)