def RCL(cpu, dest, src):
        """
        Rotates through carry left.

        Shifts (rotates) the bits of the first operand (destination operand) the number of bit positions specified in the
        second operand (count operand) and stores the result in the destination operand. The destination operand can be
        a register or a memory location; the count operand is an unsigned integer that can be an immediate or a value in
        the CL register. In legacy and compatibility mode, the processor restricts the count to a number between 0 and 31
        by masking all the bits in the count operand except the 5 least-significant bits.

        The RCL instruction shifts the CF flag into the least-significant bit and shifts the most-significant bit into the CF flag.

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
        tempCount = Operators.ZEXTEND((count & countMask) % (src.size + 1), OperandSize)

        value = dest.read()

        if isinstance(tempCount, int) and tempCount == 0:
            # this is a no-op
            new_val = value
            dest.write(new_val)
        else:
            carry = Operators.ITEBV(OperandSize, cpu.CF, 1, 0)
            right = value >> (OperandSize - tempCount)
            new_val = (value << tempCount) | (carry << (tempCount - 1)) | (right >> 1)
            dest.write(new_val)

            def sf(v, size):
                return (v & (1 << (size - 1))) != 0
            cpu.CF = sf(value << (tempCount - 1), OperandSize)
            cpu.OF = Operators.ITE(tempCount == 1,
                                   sf(new_val, OperandSize) != cpu.CF,
                                   cpu.OF)