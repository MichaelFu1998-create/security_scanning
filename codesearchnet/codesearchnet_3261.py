def JA(cpu, target):
        """
        Jumps short if above.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, Operators.AND(cpu.CF == False, cpu.ZF == False), target.read(), cpu.PC)