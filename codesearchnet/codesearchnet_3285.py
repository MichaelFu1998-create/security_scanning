def ROL(cpu, dest, src):
        """
        Rotates left (ROL).

        Shifts (rotates) the bits of the first operand (destination operand) the number of bit positions specified in the
        second operand (count operand) and stores the result in the destination operand. The destination operand can be
        a register or a memory location; the count operand is an unsigned integer that can be an immediate or a value in
        the CL register. In legacy and compatibility mode, the processor restricts the count to a number between 0 and 31
        by masking all the bits in the count operand except the 5 least-significant bits.

        The rotate left shift all the bits toward more-significant bit positions, except for the most-significant bit, which
        is rotated to the least-significant bit location.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: count operand.
        """
        OperandSize = dest.size
        count = src.read()
        countMask = {8: 0x1f,
                     16: 0x1f,
                     32: 0x1f,
                     64: 0x3f}[OperandSize]
        tempCount = Operators.ZEXTEND((count & countMask) % (OperandSize), OperandSize)

        value = dest.read()
        newValue = (value << tempCount) | (value >> (OperandSize - tempCount))
        dest.write(newValue)

        cpu.CF = Operators.ITE(tempCount != 0, (newValue & 1) == 1, cpu.CF)
        s_MSB = ((newValue >> (OperandSize - 1)) & 0x1) == 1
        cpu.OF = Operators.ITE(tempCount == 1, s_MSB ^ cpu.CF, cpu.OF)