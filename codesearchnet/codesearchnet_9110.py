def assemble(asmcode, pc=0, fork=DEFAULT_FORK):
    """ Assemble an EVM program

        :param asmcode: an evm assembler program
        :type asmcode: str
        :param pc: program counter of the first instruction(optional)
        :type pc: int
        :param fork: fork name (optional)
        :type fork: str
        :return: the hex representation of the bytecode
        :rtype: str

        Example use::

            >>> assemble('''PUSH1 0x60\n \
                                   BLOCKHASH\n \
                                   MSTORE\n \
                                   PUSH1 0x2\n \
                                   PUSH2 0x100\n \
                                ''')
            ...
            b"\x60\x60\x60\x40\x52\x60\x02\x61\x01\x00"
    """
    return b''.join(x.bytes for x in assemble_all(asmcode, pc=pc, fork=fork))