def SARX(cpu, dest, src, count):
        """
        The shift arithmetic right.

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
        tempCount = count & countMask
        tempDest = value = src.read()

        sign = value & (1 << (OperandSize - 1))
        while tempCount != 0:
            cpu.CF = (value & 0x1) != 0  # LSB
            value = (value >> 1) | sign
            tempCount = tempCount - 1
        res = dest.write(value)