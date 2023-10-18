def JNG(cpu, target):
        """
        Jumps short if not greater.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, Operators.OR(cpu.ZF, cpu.SF != cpu.OF), target.read(), cpu.PC)