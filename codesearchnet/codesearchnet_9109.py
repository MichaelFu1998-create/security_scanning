def disassemble(bytecode, pc=0, fork=DEFAULT_FORK):
    """ Disassemble an EVM bytecode

        :param bytecode: binary representation of an evm bytecode
        :type bytecode: str | bytes | bytearray
        :param pc: program counter of the first instruction(optional)
        :type pc: int
        :param fork: fork name (optional)
        :type fork: str
        :return: the text representation of the assembler code

        Example use::

            >>> disassemble("\x60\x60\x60\x40\x52\x60\x02\x61\x01\x00")
            ...
            PUSH1 0x60
            BLOCKHASH
            MSTORE
            PUSH1 0x2
            PUSH2 0x100

    """
    return '\n'.join(map(str, disassemble_all(bytecode, pc=pc, fork=fork)))