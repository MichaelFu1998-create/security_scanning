def JZ(cpu, target):
        """
        Jumps short if zero.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, cpu.ZF, target.read(), cpu.PC)