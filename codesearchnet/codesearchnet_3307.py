def PSHUFW(cpu, op0, op1, op3):
        """
        Packed shuffle words.

        Copies doublewords from source operand (second operand) and inserts them in the destination operand
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
        assert size == 64
        arg0 |= ((arg1 >> ((arg3 >> 0) & 3 * 16)) & 0xffff)
        arg0 |= ((arg1 >> ((arg3 >> 2) & 3 * 16)) & 0xffff) << 16
        arg0 |= ((arg1 >> ((arg3 >> 4) & 3 * 16)) & 0xffff) << 32
        arg0 |= ((arg1 >> ((arg3 >> 6) & 3 * 16)) & 0xffff) << 48
        op0.write(arg0)