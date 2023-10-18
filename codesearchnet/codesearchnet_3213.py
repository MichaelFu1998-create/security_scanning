def BSWAP(cpu, dest):
        """
        Byte swap.

        Reverses the byte order of a 32-bit (destination) register: bits 0 through
        7 are swapped with bits 24 through 31, and bits 8 through 15 are swapped
        with bits 16 through 23. This instruction is provided for converting little-endian
        values to big-endian format and vice versa.
        To swap bytes in a word value (16-bit register), use the XCHG instruction.
        When the BSWAP instruction references a 16-bit register, the result is
        undefined::

            TEMP  =  DEST
            DEST[7..0]  =  TEMP[31..24]
            DEST[15..8]  =  TEMP[23..16]
            DEST[23..16]  =  TEMP[15..8]
            DEST[31..24]  =  TEMP[7..0]

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        parts = []
        arg0 = dest.read()
        for i in range(0, dest.size, 8):
            parts.append(Operators.EXTRACT(arg0, i, 8))

        dest.write(Operators.CONCAT(8 * len(parts), *parts))