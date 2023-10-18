def assemble_hex(asmcode, pc=0, fork=DEFAULT_FORK):
    """ Assemble an EVM program

        :param asmcode: an evm assembler program
        :type asmcode: str | iterator[Instruction]
        :param pc: program counter of the first instruction(optional)
        :type pc: int
        :param fork: fork name (optional)
        :type fork: str
        :return: the hex representation of the bytecode
        :rtype: str

        Example use::

            >>> assemble_hex('''PUSH1 0x60\n \
                                       BLOCKHASH\n \
                                       MSTORE\n \
                                       PUSH1 0x2\n \
                                       PUSH2 0x100\n \
                                    ''')
            ...
            "0x6060604052600261010"
    """
    if isinstance(asmcode, list):
        return '0x' + hexlify(b''.join([x.bytes for x in asmcode])).decode('ascii')
    return '0x' + hexlify(assemble(asmcode, pc=pc, fork=fork)).decode('ascii')