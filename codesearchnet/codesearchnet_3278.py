def JS(cpu, target):
        """
        Jumps short if sign.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, cpu.SF, target.read(), cpu.PC)