def JB(cpu, target):
        """
        Jumps short if below.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, cpu.CF == True, target.read(), cpu.PC)