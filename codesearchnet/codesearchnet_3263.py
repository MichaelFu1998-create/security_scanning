def JBE(cpu, target):
        """
        Jumps short if below or equal.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, Operators.OR(cpu.CF, cpu.ZF), target.read(), cpu.PC)