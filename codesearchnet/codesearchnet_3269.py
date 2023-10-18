def JGE(cpu, target):
        """
        Jumps short if greater or equal.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, (cpu.SF == cpu.OF), target.read(), cpu.PC)