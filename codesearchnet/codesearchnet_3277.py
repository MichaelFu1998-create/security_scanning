def JP(cpu, target):
        """
        Jumps short if parity.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, cpu.PF, target.read(), cpu.PC)