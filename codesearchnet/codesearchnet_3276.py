def JO(cpu, target):
        """
        Jumps short if overflow.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, cpu.OF, target.read(), cpu.PC)