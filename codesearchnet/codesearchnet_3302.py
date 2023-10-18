def SHLX(cpu, dest, src, count):
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
        count = count.read()
        countMask = {8: 0x1f,
                     16: 0x1f,
                     32: 0x1f,
                     64: 0x3f}[OperandSize]
        tempCount = Operators.ZEXTEND(count & countMask, dest.size)
        tempDest = value = src.read()
        res = dest.write(Operators.ITEBV(dest.size, tempCount == 0, tempDest, value << tempCount))