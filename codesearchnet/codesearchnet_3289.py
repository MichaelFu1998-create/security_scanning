def SHLD(cpu, dest, src, count):
        """
        Double precision shift right.

        Shifts the first operand (destination operand) to the left the number of bits specified by the third operand
        (count operand). The second operand (source operand) provides bits to shift in from the right (starting with
        the least significant bit of the destination operand).

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        :param count: count operand
        """
        OperandSize = dest.size
        tempCount = Operators.ZEXTEND(count.read(), OperandSize) & (OperandSize - 1)
        arg0 = dest.read()
        arg1 = src.read()

        MASK = ((1 << OperandSize) - 1)
        t0 = (arg0 << tempCount)
        t1 = arg1 >> (OperandSize - tempCount)
        res = Operators.ITEBV(OperandSize, tempCount == 0, arg0, t0 | t1)
        res = res & MASK
        dest.write(res)
        if isinstance(tempCount, int) and tempCount == 0:
            pass
        else:
            SIGN_MASK = 1 << (OperandSize - 1)
            lastbit = 0 != ((arg0 << (tempCount - 1)) & SIGN_MASK)

            cpu._set_shiftd_flags(OperandSize, arg0, res, lastbit, tempCount)