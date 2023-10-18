def JC(cpu, target):
        """
        Jumps short if carry.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, cpu.CF, target.read(), cpu.PC)