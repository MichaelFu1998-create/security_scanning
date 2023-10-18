def PMOVMSKB(cpu, op0, op1):
        """
        Moves byte mask to general-purpose register.

        Creates an 8-bit mask made up of the most significant bit of each byte of the source operand
        (second operand) and stores the result in the low byte or word of the destination operand
        (first operand). The source operand is an MMX(TM) technology or an XXM register; the destination
        operand is a general-purpose register.

        :param cpu: current CPU.
        :param op0: destination operand.
        :param op1: source operand.
        """
        arg0 = op0.read()
        arg1 = op1.read()

        res = 0
        for i in reversed(range(7, op1.size, 8)):
            res = (res << 1) | ((arg1 >> i) & 1)
        op0.write(Operators.EXTRACT(res, 0, op0.size))