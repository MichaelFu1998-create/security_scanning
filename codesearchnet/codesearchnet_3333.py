def VPSHUFB(cpu, op0, op1, op3):
        """
        Packed shuffle bytes.

        Copies bytes from source operand (second operand) and inserts them in the destination operand
        (first operand) at locations selected with the order operand (third operand).

        :param cpu: current CPU.
        :param op0: destination operand.
        :param op1: source operand.
        :param op3: order operand.
         """
        size = op0.size
        arg0 = op0.read()
        arg1 = op1.read()
        arg3 = Operators.ZEXTEND(op3.read(), size)

        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 7, 1) == 1, 0, (arg1 >> ((arg3 >> 0) & 7 * 8)) & 0xff)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 15, 1) == 1, 0, ((arg1 >> ((arg3 >> 8) & 7 * 8)) & 0xff) << 8)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 23, 1) == 1, 0, ((arg1 >> ((arg3 >> 16) & 7 * 8)) & 0xff) << 16)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 31, 1) == 1, 0, ((arg1 >> ((arg3 >> 24) & 7 * 8)) & 0xff) << 24)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 39, 1) == 1, 0, ((arg1 >> ((arg3 >> 32) & 7 * 8)) & 0xff) << 32)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 47, 1) == 1, 0, ((arg1 >> ((arg3 >> 40) & 7 * 8)) & 0xff) << 40)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 55, 1) == 1, 0, ((arg1 >> ((arg3 >> 48) & 7 * 8)) & 0xff) << 48)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 63, 1) == 1, 0, ((arg1 >> ((arg3 >> 56) & 7 * 8)) & 0xff) << 56)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 71, 1) == 1, 0, ((arg1 >> ((arg3 >> 64) & 7 * 8)) & 0xff) << 64)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 79, 1) == 1, 0, ((arg1 >> ((arg3 >> 72) & 7 * 8)) & 0xff) << 72)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 87, 1) == 1, 0, ((arg1 >> ((arg3 >> 80) & 7 * 8)) & 0xff) << 80)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 95, 1) == 1, 0, ((arg1 >> ((arg3 >> 88) & 7 * 8)) & 0xff) << 88)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 103, 1) == 1, 0, ((arg1 >> ((arg3 >> 96) & 7 * 8)) & 0xff) << 96)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 111, 1) == 1, 0, ((arg1 >> ((arg3 >> 104) & 7 * 8)) & 0xff) << 104)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 119, 1) == 1, 0, ((arg1 >> ((arg3 >> 112) & 7 * 8)) & 0xff) << 112)
        arg0 |= Operators.ITEBV(size, Operators.EXTRACT(arg3, 127, 1) == 1, 0, ((arg1 >> ((arg3 >> 120) & 7 * 8)) & 0xff) << 120)
        op0.write(arg0)