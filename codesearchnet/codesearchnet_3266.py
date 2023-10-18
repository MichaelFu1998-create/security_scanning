def JECXZ(cpu, target):
        """
        Jumps short if ECX register is 0.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, cpu.ECX == 0, target.read(), cpu.PC)