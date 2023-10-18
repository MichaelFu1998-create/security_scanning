def JG(cpu, target):
        """
        Jumps short if greater.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, Operators.AND(cpu.ZF == False, cpu.SF == cpu.OF), target.read(), cpu.PC)