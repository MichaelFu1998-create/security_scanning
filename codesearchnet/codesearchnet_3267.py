def JRCXZ(cpu, target):
        """
        Jumps short if RCX register is 0.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, cpu.RCX == 0, target.read(), cpu.PC)