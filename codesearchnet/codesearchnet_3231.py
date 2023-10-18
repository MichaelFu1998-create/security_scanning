def MOVBE(cpu, dest, src):
        """
        Moves data after swapping bytes.

        Performs a byte swap operation on the data copied from the second operand (source operand) and store the result
        in the first operand (destination operand). The source operand can be a general-purpose register, or memory location; the destination register can be a general-purpose register, or a memory location; however, both operands can
        not be registers, and only one operand can be a memory location. Both operands must be the same size, which can
        be a word, a doubleword or quadword.
        The MOVBE instruction is provided for swapping the bytes on a read from memory or on a write to memory; thus
        providing support for converting little-endian values to big-endian format and vice versa.
        In 64-bit mode, the instruction's default operation size is 32 bits. Use of the REX.R prefix permits access to additional registers (R8-R15). Use of the REX.W prefix promotes operation to 64 bits::

                TEMP = SRC
                IF ( OperandSize = 16)
                THEN
                    DEST[7:0] = TEMP[15:8];
                    DEST[15:8] = TEMP[7:0];
                ELSE IF ( OperandSize = 32)
                    DEST[7:0] = TEMP[31:24];
                    DEST[15:8] = TEMP[23:16];
                    DEST[23:16] = TEMP[15:8];
                    DEST[31:23] = TEMP[7:0];
                ELSE IF ( OperandSize = 64)
                    DEST[7:0] = TEMP[63:56];
                    DEST[15:8] = TEMP[55:48];
                    DEST[23:16] = TEMP[47:40];
                    DEST[31:24] = TEMP[39:32];
                    DEST[39:32] = TEMP[31:24];
                    DEST[47:40] = TEMP[23:16];
                    DEST[55:48] = TEMP[15:8];
                    DEST[63:56] = TEMP[7:0];
                FI;

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        size = dest.size
        arg0 = dest.read()
        temp = 0
        for pos in range(0, size, 8):
            temp = (temp << 8) | (arg0 & 0xff)
            arg0 = arg0 >> 8
        dest.write(arg0)