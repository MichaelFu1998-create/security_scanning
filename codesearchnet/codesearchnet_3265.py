def JCXZ(cpu, target):
        """
        Jumps short if CX register is 0.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, cpu.CX == 0, target.read(), cpu.PC)