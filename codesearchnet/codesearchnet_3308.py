def PSHUFD(cpu, op0, op1, op3):
        """
        Packed shuffle doublewords.

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
        order = Operators.ZEXTEND(op3.read(), size)

        arg0 = arg0 & 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000
        arg0 |= ((arg1 >> (((order >> 0) & 3) * 32)) & 0xffffffff)
        arg0 |= ((arg1 >> (((order >> 2) & 3) * 32)) & 0xffffffff) << 32
        arg0 |= ((arg1 >> (((order >> 4) & 3) * 32)) & 0xffffffff) << 64
        arg0 |= ((arg1 >> (((order >> 6) & 3) * 32)) & 0xffffffff) << 96

        op0.write(arg0)