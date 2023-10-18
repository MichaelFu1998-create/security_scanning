def SAL(cpu, dest, src):
        """
        The shift arithmetic left.

        Shifts the bits in the first operand (destination operand) to the left or right by the number of bits specified in the
        second operand (count operand). Bits shifted beyond the destination operand boundary are first shifted into the CF
        flag, then discarded. At the end of the shift operation, the CF flag contains the last bit shifted out of the destination
        operand.

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
        tempCount = Operators.ZEXTEND(count & countMask, dest.size)

        tempDest = value = dest.read()
        res = dest.write(Operators.ITEBV(dest.size, tempCount == 0, tempDest, value << tempCount))

        # Should not modify flags if tempcount == 0
        MASK = (1 << OperandSize) - 1
        SIGN_MASK = 1 << (OperandSize - 1)

        cpu.CF = Operators.OR(Operators.AND(tempCount == 0, cpu.CF), Operators.AND(tempCount != 0, (tempDest & (1 << (OperandSize - tempCount)) != 0)))
        # OF is only set iff count == 1, and set to XOR(CF, MSB(res))
        # OF is only defined for count == 1, but in practice (unit tests from real cpu) its calculated for count != 0
        cpu.OF = Operators.ITE(tempCount != 0, (cpu.CF) ^ (((res >> (OperandSize - 1)) & 0x1) == 1), cpu.OF)
        cpu.SF = Operators.OR(Operators.AND(tempCount == 0, cpu.SF), Operators.AND(tempCount != 0, (res & SIGN_MASK) != 0))
        cpu.ZF = Operators.OR(Operators.AND(tempCount == 0, cpu.ZF), Operators.AND(tempCount != 0, res == 0))
        cpu.PF = Operators.OR(Operators.AND(tempCount == 0, cpu.PF), Operators.AND(tempCount != 0, cpu._calculate_parity_flag(res)))