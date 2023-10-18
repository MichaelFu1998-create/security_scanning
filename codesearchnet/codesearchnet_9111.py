def disassemble_hex(bytecode, pc=0, fork=DEFAULT_FORK):
    """ Disassemble an EVM bytecode

        :param bytecode: canonical representation of an evm bytecode (hexadecimal)
        :type bytecode: str
        :param pc: program counter of the first instruction(optional)
        :type pc: int
        :param fork: fork name (optional)
        :type fork: str
        :return: the text representation of the assembler code
        :rtype: str

        Example use::

            >>> disassemble_hex("0x6060604052600261010")
            ...
            PUSH1 0x60
            BLOCKHASH
            MSTORE
            PUSH1 0x2
            PUSH2 0x100

    """
    if bytecode.startswith('0x'):
        bytecode = bytecode[2:]
    bytecode = unhexlify(bytecode)
    return disassemble(bytecode, pc=pc, fork=fork)