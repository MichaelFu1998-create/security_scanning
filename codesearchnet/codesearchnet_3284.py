def RCR(cpu, dest, src):
        """
        Rotates through carry right (RCR).

        Shifts (rotates) the bits of the first operand (destination operand) the number of bit positions specified in the
        second operand (count operand) and stores the result in the destination operand. The destination operand can be
        a register or a memory location; the count operand is an unsigned integer that can be an immediate or a value in
        the CL register. In legacy and compatibility mode, the processor restricts the count to a number between 0 and 31
        by masking all the bits in the count operand except the 5 least-significant bits.

        Rotate through carry right (RCR) instructions shift all the bits toward less significant bit positions, except
        for the least-significant bit, which is rotated to the most-significant bit location. The RCR instruction shifts the
        CF flag into the most-significant bit and shifts the least-significant bit into the CF flag.

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
            left = value >> (tempCount - 1)
            right = value << (OperandSize - tempCount)

            new_val = (left >> 1) | (carry << (OperandSize - tempCount)) | (right << 1)

            dest.write(new_val)

            cpu.CF = Operators.ITE(tempCount != 0, (left & 1) == 1, cpu.CF)
            # for RCR these are calculated before rotation starts
            s_MSB = ((new_val >> (OperandSize - 1)) & 0x1) == 1
            s_MSB2 = ((new_val >> (OperandSize - 2)) & 0x1) == 1
            cpu.OF = Operators.ITE(tempCount == 1,
                                   s_MSB ^ s_MSB2, cpu.OF)