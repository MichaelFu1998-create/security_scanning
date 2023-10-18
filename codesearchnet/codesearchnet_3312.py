def MOVSX(cpu, op0, op1):
        """
        Moves with sign-extension.

        Copies the contents of the source operand (register or memory location) to the destination
        operand (register) and sign extends the value to 16::

                OP0  =  SignExtend(OP1);

        :param cpu: current CPU.
        :param op0: destination operand.
        :param op1: source operand.
        """
        op0.write(Operators.SEXTEND(op1.read(), op1.size, op0.size))