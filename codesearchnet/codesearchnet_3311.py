def MOVZX(cpu, op0, op1):
        """
        Moves with zero-extend.

        Copies the contents of the source operand (register or memory location) to the destination
        operand (register) and zero extends the value to 16 or 32 bits. The size of the converted value
        depends on the operand-size attribute::

                OP0  =  ZeroExtend(OP1);

        :param cpu: current CPU.
        :param op0: destination operand.
        :param op1: source operand.
        """
        op0.write(Operators.ZEXTEND(op1.read(), op0.size))